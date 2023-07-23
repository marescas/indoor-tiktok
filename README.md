# Indoor TikTok

The objective of this repo is to create a simple image content retrival system using Vespa.
This is not a Production system and has many points of improvements specially in how to index (batching) and the quality
of the embeddings that are indexed.

Be aware that this project has been created during some free time during summer
weekends (suffering almost 35º degrees
in the beautiful Valencia). Don't expect any good practices ;)

## Why indoor TikTok?

When I was starting the project I was thinking on building a simple app to demonstrate that a user can provide feedback
if he likes/dislike an image and I can refine the search using the embeddings of the like/dislike images. For that, I
realized that first I need all the building blocks. So my idea is to update the repo with new features once I have free
time ;)

## How to execute
If you want to execute the project you need to:

* Download the dataset https://www.kaggle.com/datasets/itsahmad/indoor-scenes-cvpr-2019 and create a folder with all the
  Images
* Create a virtualenv and install requirements.txt
* Be sure that the PYTHONPATH is set correctly `export PYTHONPATH="$PWD"`
* Execute the `define_vespa.py` script inside vespa folder. Be sure you have Docker
* Execute the `embedding_service.py` script
* Execute `indexer.py` inside the indexer folder. Be sure you have the folder `Images` with your dataset and the
  embedding service / vespa are ready
* execute the frontend by running `streamlit run frontend/frontend.py`
* Enjoy

## Feedback

Any errors or improvements. Feel free to reach me on Twitter @mecprojects or my email marescasinf@gmail.com

