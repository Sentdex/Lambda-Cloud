# Lambda-Cloud
Helpers and such for working with Lambda Cloud.

# Setup process for a new instance:
May eventually have different setup processes depending on the use-case, but for now:
Either copy over the llm-setup.sh file or:

`$ nano llm-setup.sh`

```
#!/bin/bash
sudo pip3 install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
sudo pip3 install --upgrade huggingface-hub
sudo pip3 install --upgrade transformers einops accelerate
sudo pip3 install xformers
sudo pip3 install --upgrade bitsandbytes
sudo pip3 install flask
sudo pip3 install python-dotenv
export LD_LIBRARY_PATH=/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
```

`$ chmod +x setup.sh`


`$./setup.sh`

# .env file

You may not need everything included in the example. `LAMBDA_KEY` is your Lambda cloud API key, which allows you to spin up, check, terminate...etc instances. `LAMBDA_SSH_KEY_NAME` is the name of your ssh key file on Lambda cloud, so the API knows which key to associate with an instance you spin up. Finally `HF_AUTH` is used for any LLM that you may wish to DL/use on Lambda that requires authorization to use. 

