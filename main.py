import os
import json
import math
import torch
from torch import nn
from torch.nn import functional as F
from torch.utils.data import DataLoader
import commons
import utils
from data_utils import TextAudioLoader, TextAudioCollate, TextAudioSpeakerLoader, TextAudioSpeakerCollate
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
from scipy.io.wavfile import write
import discord
import json
import g4f

# Config
speaker = '胡桃' # Choose from NPC List Below
client_secret = 'MTAyODE3MjYxNjg2OTEwMTU3OQ.Gkmsbq.u9b04vLYl1OU_uSXUfbgSXrIkMHGRqBFYPfjbs'
model_path = './model/G_809000.pth'
output_path = "./output.mp3"

# NPC List
npcList = ['派蒙', '凯亚', '安柏', '丽莎', '琴', '香菱', '枫原万叶',
           '迪卢克', '温迪', '可莉', '早柚', '托马', '芭芭拉', '优菈',
           '云堇', '钟离', '魈', '凝光', '雷电将军', '北斗',
           '甘雨', '七七', '刻晴', '神里绫华', '戴因斯雷布', '雷泽',
           '神里绫人', '罗莎莉亚', '阿贝多', '八重神子', '宵宫',
           '荒泷一斗', '九条裟罗', '夜兰', '珊瑚宫心海', '五郎',
           '散兵', '女士', '达达利亚', '莫娜', '班尼特', '申鹤',
           '行秋', '烟绯', '久岐忍', '辛焱', '砂糖', '胡桃', '重云',
           '菲谢尔', '诺艾尔', '迪奥娜', '鹿野院平藏']

# Process text
def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm

# Loads model config
hps_mt = utils.get_hparams_from_file("./configs/genshin.json")

net_g_mt = SynthesizerTrn(
    len(symbols),
    hps_mt.data.filter_length // 2 + 1,
    hps_mt.train.segment_size // hps_mt.data.hop_length,
    n_speakers=hps_mt.data.n_speakers,
    **hps_mt.model)
_ = net_g_mt.eval()

_ = utils.load_checkpoint(model_path, net_g_mt, None)


# Discord.py
intents = intents = discord.Intents().all()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

response_memory = ""

@client.event
async def on_message(message):
    global response_memory
    if message.author == client.user:
        return
    elif speaker in message.content:
        #Change nickname of bot
        await message.guild.me.edit(nick=speaker)

        # Memory of last response
        if(response_memory):
            response_memory = "上一句你回答了：'" + response_memory + "'。"

        #Generate Response
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": "现在，请扮演原神里的" + speaker + ",我则是旅行者，请让对话保持50字以内(包括标点符号),只用原神游戏里的知识并只用中文回答。" + response_memory + message.content}],
        )
        response = response[:50]
        response_memory = response

        #Generate Voice
        t_mt= response
        stn_tst_mt = get_text(t_mt.replace("\n", ""), hps_mt)
        print(stn_tst_mt)

        with torch.no_grad():
            x_tst_mt = stn_tst_mt.unsqueeze(0)
            x_tst_mt_lengths = torch.LongTensor([stn_tst_mt.size(0)])
            sid_mt = torch.LongTensor([npcList.index(speaker)])
            audio_mt = net_g_mt.infer(x_tst_mt, x_tst_mt_lengths, sid=sid_mt, noise_scale=.667, noise_scale_w=.8, length_scale=1.2)[0][0,0].data.cpu().float().numpy()
            write(output_path, hps_mt.data.sampling_rate, audio_mt)

        #Send message    
        channel = message.channel  
        await channel.send(response)
        await channel.send(file=discord.File(output_path))

client.run(client_secret)