from django.shortcuts import render

from .models import Product

from etsy2 import Etsy
import json

# this is where the response retrieved will be stored everytime
# we request something from the API
globalResponse = []

# Create your views here.
# A function based view
def productPage(request):

	# this holds information about the first product created within our
	# database, hence the id = 1
	obj1 = Product.objects.get(id=1)

	context = {'pencil': obj1}
	return render(request, 'prod/home.html', context)


def allProductsPage(request):

	# this holds all the products within our database
	obj1 = Product.objects.all()

	context = {'pencil': obj1}
	return render(request, 'prod/AllProducts.html', context)


def productsFromEtsyAPI(request):

	# etsy object
	etsy = Etsy(api_key="iithgv8q30ciefkkxlna5oai")
	response = etsy.findAllListingActive(limit = 3)
	globalResponse = response
	print("New Link is", type(response[0]["url"]))

	# extract all the listing ids from all products in our database
	allProductIDS = [product.listing_id for product in Product.objects.all()]


	#######################
	# allProductsIDS = []
	# for product in Product.objects.all():
	# 	allProductsIDS.append(product.listing_id)
	#######################

	for index in range(len(response)):
		# makes sure we don't add duplicate items into our database
		if response[index]["listing_id"] in allProductIDS:
			continue # continue skips the else clause and goes to the next iteration
		else:
			newTitle = response[index].get("title")
			newDescription = response[index].get("description")
			newPrice = response[index].get("price")
			productListingId = response[index]["listing_id"]
			newLink = response[index]["url"]

			Product.objects.create(title = newTitle, description = newDescription,
				price = newPrice, listing_id = productListingId, productLink = newLink)
			getImageByListingID(etsy, productListingId)

	# this holds all the products within our database
	obj1 = Product.objects.all()
	print(obj1[0].productLink)

	context = {'APIproducts': obj1}
	return render(request, 'prod/EtsyAPI.html', context)

# def filterListingIds(request):
# 	allListingIds = []

# 	for listing in globalResponse:
# 		# retrieving the id for a listing which is stored in a dictionary
# 		allListingIds = listing["listing_id"]


# we have to obtain the images associated to a listing first, and then pick one
# of the images to attach to our object created in our database
def getImageByListingID(etsyObject, listing_id):

	# this method findAllListingImages is provided by the Etsy API, and
	# the only parameter needed to obtain the images is just the listing_id
	# which our response within the productsFromEtsyAPI method comes with ....
	# i.e. first (key,value) pair in every dictionary of the response list
	imagesFromAPI = etsyObject.findAllListingImages(listing_id=listing_id)

	# open a folder based on where our static files are created and
	# name the folders according the listing_id of products so when
	# images are to be uploaded, we can access them correctly
	print("This is the result I'm referring to", imagesFromAPI)
