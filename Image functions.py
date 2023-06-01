def extract_images(link):
    print(link)
    response = html_parser(link)
    images = response.find_all('img')
    for image in images:
        name_image = image['alt'].replace(":", " ").replace("/", " ").replace("\"", " ").replace("*", " ")\
            .replace("?", " ").lstrip()
        link_image = f'{constants.url}/' + image['src'].lstrip('./')
        with open(name_image + '.jpg', 'wb') as file:
            img = requests.get(link_image)
            file.write(img.content)
            print('Writing: ', name_image)
            print(link_image)

