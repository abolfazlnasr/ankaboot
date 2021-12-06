import numpy as np
from PIL import Image
from wordcloud_fa import WordCloudFa


def create_wordcloud_from_text(text):
    mask = np.array(Image.open("img/cloud.png"))
    wordcloud = WordCloudFa(persian_normalize=True, include_numbers=False, background_color="white", mask=mask)
    result = wordcloud.generate(text)
    image = result.to_image()
    image.save("img/result.png", format="png")
