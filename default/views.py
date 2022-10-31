import os
import sys
import shutil
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import json
from threading import Thread
from time import sleep
from DeepImageSearch import Index,LoadData,SearchImage
from .models import Item
import requests
# Create your views here.
newImage = False
images_array = []
def checkImages(newImage):
    print(len(images_array))
    print(len(images_array))
    print(len(images_array))
    print(len(images_array))
    print(len(images_array))
    database_items_length = Item.objects.all().count()
    print(database_items_length)
    print(database_items_length)
    print(database_items_length)
    print(database_items_length)
    directory = settings.MEDIA_ROOT + "/images"
    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            #print(f)
            if f not in images_array:
                images_array.append(f)
                newImage = True
    if(newImage == True or database_items_length != len(images_array)):
        mydir = "meta-data-files"
        try:
            shutil.rmtree(mydir)
            print("folder deleted")
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
            
        image_list = LoadData().from_folder(['./media/images'])
        # For Faster Serching we need to index Data first
        print("indexing the data for faster searching")
        Index(image_list).Start()
        
    print(images_array)
    newImage = False#overide the new image to false now after training the data
def background_task(interval_sec):
    while True:
        # block for the interval
        print('Starting background task in 10 seconds...')
        sleep(interval_sec)
        checkImages(newImage = newImage)
        # perform the task
        print('Background task completed!')
# create and start the daemon thread
daemon = Thread(target=background_task, args=(10,), daemon=True, name='Background')
daemon.start()

def searchImagesNow(image):
    #image_list = LoadData().from_folder(['./media/images'])
    # For Faster Serching we need to index Data first
    #Index(image_list).Start()
    # for searching
    image_list_length = LoadData().from_folder(['./media/images'])
    print(len(image_list_length))
    data = SearchImage().get_similar_images(image_path=image,number_of_images=len(image_list_length))
    print(data)
    tosend = []
    for x in data:
        tosend.append({"image":data[x]})
    return json.dumps(tosend)
    """
    data = SearchImage().get_similar_images(image_path=image,number_of_images=5)
    print(data)
    #deletion of the folder which was created for faster image searching of the data
    mydir = "meta-data-files"
    tosend = []
    try:
        shutil.rmtree(mydir)
        print("folder deleted")
        for x in data:
            tosend.append({"image":data[x]})
        return {"message":"success", "data":tosend}
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        return {"message":"error", "data":"Error: %s - %s." % (e.filename, e.strerror)}
    """
def home_view(request, *args, **kwargs):
    if request.method == "POST":
        image = request.FILES['image_search']
        while newImage == True:
            print("New Images have been added to the directory, we are indexing the data")
            sleep(1)

        while os.path.exists("meta-data-files") == False:
            print("waiting for directory to be created")

        message = searchImagesNow(image = image)
        print(message)
        print(message)
        datas = json.loads(message)
        for x in datas:
            print(x)
            print(str(x['image']).replace(r"./media/images", "")[1:])
            databaseItem = Item.objects.filter(cover='images/'+str(x['image']).replace(r"./media/images", "")[1:]).first()
            x.update({"name":databaseItem.name})
            x.update({"description":databaseItem.description})
            print(databaseItem)
            """
            newData.append(
                {
                    "image":x['image'],
                    "name":databaseItem.name,
                    "description":databaseItem.description
                }
            )
            """
        print(datas)
        return HttpResponse(json.dumps(datas))
    items = Item.objects.order_by("?")
    context = {
        "items":items
    }
    response = render(request, "index.html", context)
    return response


def delete_view(request, *args, **kwargs):
    try:
        id = request.GET.get("id")
        item = Item.objects.get(id=id)
        if item.cover != "images/default.jpg":
            item.cover.delete()
        item.delete()
        images_array.clear()
        print(images_array)
    except:
        return HttpResponse(json.dumps({"message":"failure to delete"}))
    return HttpResponse(json.dumps({"message":"item deleted"}))


def saveImages():
    url = 'http://127.0.0.1:8000/media/images/car3.jfif'
    page = requests.get(url)

    f_ext = os.path.splitext(url)[-1]
    print(url.rindex("/"))
    print(url.rindex("."))
    print(url[url.rindex("/")+1:url.rindex(".")])
    f_name = '{}{}'.format(url[url.rindex("/")+1:url.rindex(".")],f_ext)
    with open(f_name, 'wb') as f:
        f.write(page.content)