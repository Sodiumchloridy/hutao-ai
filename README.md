
# Hutao Voice
A Discord chatbot based on characters from Genshin Impact that utilizes g4f and VITS to generate chat responses along with the character's voice. Currently only supports Chinese voicelines because I got the pre-trained voice model from the web, reserved my kidney for the iPhone instead of the latest NVIDIA graphics card.

一款基于《原神》角色的Discord聊天机器人，利用g4f和VITS生成聊天响应以及角色的声音。目前只支持中文语音线因为语音模型是我从网上别人那里拿来的，将我的肾脏保留给了iPhone而不是最新的NVIDIA显卡。

## Demo

Note: Kindly turn up the volume for best experience.

注意：为获得最佳体验，请将音量调高。


https://github-production-user-asset-6210df.s3.amazonaws.com/67376832/277171484-c0c48596-8f43-4f84-8772-f7d8146fe4e8.mp4

## Getting Started

Clone and setup hutao-voice with pip. Python 3.8 is required, or Miniconda 3 for Python 3.8.

克隆和使用 pip 设置 Hutao Voice。需要 Python 3.8 或 Miniconda 3 以支持 Python 3.8。


```bash
  git clone https://github.com/Sodiumchloridy/hutao-voice.git
  cd hutao-voice
  pip install -r "requirements.txt"
  cd monotonic_align
  python setup.py build_ext --inplace
```

Set the environmental variables with your Discord Bot Token (**[Guide](https://discordjs.guide/preparations/setting-up-a-bot-application.html#creating-your-bot)**) in `main.py`. You can choose a character's voice from the list of characters available by setting `speaker` to your desired character.

在 `main.py` 中设置 Discord 机器人令牌的环境变量 (**[参考指南](https://discordjs.guide/preparations/setting-up-a-bot-application.html#creating-your-bot)**)。你可以通过将 `speaker` 设置为你想要的角色来选择一个角色的声音。

```javascript
client_secret = 'YOUR_DICORD_BOT_TOKEN'
speaker = '胡桃'
```

Note: Make sure to use `.env` files if you plan to upload it to a git repository. To run the file:

注意：如果你计划上传到 Git 存储库，请确保使用`.env`文件来保存敏感信息。要运行该文件，请按以下步骤操作：

`python main.py`

Now your Discord Bot should be up and running!

现在你的 Discord 机器人应该已经准备就绪并运行了！
## Usage/Examples

The usage of the bot varies by the character's voice that you've chosen. As for the default with `胡桃` (Hu Tao) being chosen set as the `speaker`, an example will be: "胡桃 good morning!" However, the bot should reply only in Chinese as tweaked, this is not a bug, it's a feature, trust.

关于机器人的使用方式会根据你选择的角色的声音而有所不同。对于默认选择 `胡桃` 作为 `speaker` 的情况，一个示例会是："胡桃 早安！" 但胡桃应该只以中文回复。
## Appendix

The voice synthesizer is defaulted to use CPU instead of your dedicated graphics card for processing. You may tweak the code to use the CUDA cores from your graphcis card for a much faster performance.

声音合成器默认使用 CPU 进行处理，而不是使用你的独立显卡的 CUDA 核心，你可以调整代码以利用显卡的 CUDA 核心来实现更快的性能。
