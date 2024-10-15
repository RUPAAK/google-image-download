import bs4
import requests
import shutil
import os

GOOGLE_IMAGE = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'
IMG_EXTENSIONS = ['.png', '.jpg', '.jfif', '.svg']


def get_image_extension(url):
    """Returns the correct file extension based on the image URL."""
    ext = os.path.splitext(url)[-1].lower()
    return ext if ext in IMG_EXTENSIONS else '.jpg'  # Default to '.jpg' if unknown


def fetch_image_links(search_query):
    URL_input = f"{GOOGLE_IMAGE}q={search_query}"
    response = requests.get(URL_input)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    return [img.get('src') for img in soup.find_all('img') if img.get('src')]


def download_images(image_links, quantity):
    if not os.path.exists('data'):
        os.makedirs('data')

    for i, link in enumerate(image_links[:quantity]):
        print(link.startswith('https://'))
        if link.startswith('https://'):
            ext = get_image_extension(link)
            filename = f'data/{i}{ext}'
            response = requests.get(link, stream=True)
            with open(filename, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
                
    print('Downloaded Finish...')


def main():
    search_query = input('What are you looking for: ')
    quantity = int(input('How many do you want: '))
    image_links = fetch_image_links(search_query)
    download_images(image_links, quantity + 1)


if __name__ == "__main__":
    main()
