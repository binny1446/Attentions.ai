import requests
import json

url = "http://127.0.0.1:5000/qa"
data = {
    "paper_text": "The Bradley-Terry (BT) model is a common and successful practice in reward\nmodeling for Large Language Model (LLM) alignment. However, it remains unclear\nwhy this model -- originally developed for multi-player stochastic game\nmatching -- can be adopted to convert pairwise response comparisons to reward\nvalues and make predictions. Especially given the fact that only a limited\nnumber of prompt-response pairs are sparsely compared with others. In this\npaper, we first revisit the foundations of using BT models in reward modeling,\nand establish the convergence rate of BT reward models based on deep neural\nnetworks using embeddings, providing a theoretical foundation for their use.\nDespite theoretically sound, we argue that the BT model is not a necessary\nchoice from the perspective of downstream optimization. This is because a\nreward model only needs to preserve the correct ranking predictions through a\nmonotonic transformation of the true reward. We highlight the critical concept\nof order consistency in reward modeling and demonstrate that the BT model\npossesses this property. Consequently, we propose a simple and straightforward\nupper-bound algorithm, compatible with off-the-shelf binary classifiers, as an\nalternative order-consistent reward modeling objective. To offer practical\ninsights, we empirically evaluate the performance of these different reward\nmodeling approaches across more than 12,000 experimental setups, using $6$ base\nLLMs, $2$ datasets, and diverse annotation designs that vary in quantity,\nquality, and pairing choices in preference annotations.",
    "question": "which model is used here?"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    print("Answer:", response.json())
else:
    print("Error:", response.status_code)