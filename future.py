import requests
import json

# URL of your Flask app's /future_work route
url = "http://127.0.0.1:5000/future_work"

# Example data (abstracts of the papers)
papers = [
    {"abstract": "With the introduction of transformer-based models for vision and language\ntasks, such as LLaVA and Chameleon, there has been renewed interest in the\ndiscrete tokenized representation of images. These models often treat image\npatches as discrete tokens, analogous to words in natural language, learning\njoint alignments between visual and human languages. However, little is known\nabout the statistical behavior of these visual languages - whether they follow\nsimilar frequency distributions, grammatical structures, or topologies as\nnatural languages. In this paper, we take a natural-language-centric approach\nto analyzing discrete visual languages and uncover striking similarities and\nfundamental differences. We demonstrate that, although visual languages adhere\nto Zipfian distributions, higher token innovation drives greater entropy and\nlower compression, with tokens predominantly representing object parts,\nindicating intermediate granularity. We also show that visual languages lack\ncohesive grammatical structures, leading to higher perplexity and weaker\nhierarchical organization compared to natural languages. Finally, we\ndemonstrate that, while vision models align more closely with natural languages\nthan other models, this alignment remains significantly weaker than the\ncohesion found within natural languages. Through these experiments, we\ndemonstrate how understanding the statistical properties of discrete visual\nlanguages can inform the design of more effective computer vision models."},
    {"abstract": "The development of large language models (LLMs) has expanded to multi-modal\nsystems capable of processing text, images, and speech within a unified\nframework. Training these models demands significantly larger datasets and\ncomputational resources compared to text-only LLMs. To address the scaling\nchallenges, we introduce Mixture-of-Transformers (MoT), a sparse multi-modal\ntransformer architecture that significantly reduces pretraining computational\ncosts. MoT decouples non-embedding parameters of the model by modality --\nincluding feed-forward networks, attention matrices, and layer normalization --\nenabling modality-specific processing with global self-attention over the full\ninput sequence. We evaluate MoT across multiple settings and model scales. In\nthe Chameleon 7B setting (autoregressive text-and-image generation), MoT\nmatches the dense baseline's performance using only 55.8\\% of the FLOPs. When\nextended to include speech, MoT reaches speech performance comparable to the\ndense baseline with only 37.2\\% of the FLOPs. In the Transfusion setting, where\ntext and image are trained with different objectives, a 7B MoT model matches\nthe image modality performance of the dense baseline with one third of the\nFLOPs, and a 760M MoT model outperforms a 1.4B dense baseline across key image\ngeneration metrics. System profiling further highlights MoT's practical\nbenefits, achieving dense baseline image quality in 47.2\\% of the wall-clock\ntime and text quality in 75.6\\% of the wall-clock time (measured on AWS\np4de.24xlarge instances with NVIDIA A100 GPUs)"}
]

# Prepare the data in the expected JSON format
data = {
    "papers": papers
}

# Send the POST request
response = requests.post(url, json=data)

# Check if the request was successful
if response.status_code == 200:
    # Extract the future work suggestions from the response
    future_work = response.json().get('future_work')
    print("Future work suggestions:", future_work)
else:
    print("Error:", response.status_code)