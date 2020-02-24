import re
import json
import requests
from dict_digger import dig
from random import random, choice
from string import ascii_letters, digits


def env_switcher(environment):
    """Gets the correct match of environment and urls"""

    # Dict of envs to URLs
    envs = {
        'prodRest': ['https://www.arcgis.com', 'https://billing.arcgis.com'],
        'qaRest': ['https://qaext.arcgis.com', 'https://billingqa.arcgis.com'],
        'devRest': ['https://devext.arcgis.com', 'https://billingdev.arcgis.com']
    }

    # Extract the url that matches the passed environment
    if environment == 'https://developers.arcgis.com':
        return envs['prodRest']

    elif environment == 'https://master-stage.developers.arcgis.com':
        return envs['qaRest']

    elif re.match('.*-dev\.developers\.arcgis\.com', environment):
        return envs['devRest']


def gen_token_via_rest(url, user, password):
    """Requests user token from ArcGIS Online Rest API.
    Uses http://www.python-requests.org/en/latest/
    for making the requests"""

    # Rest url for generating tokens
    genTokenUrl = str(url) + '/sharing/rest/generateToken'

    # Needed query string params to be added to the URL
    genTokenPayload = {
        'f': 'json',
        'username': user,
        'password': password,
        'referer': url
    }

    # Makes post call and appends params
    genTokenPost = requests.post(
        genTokenUrl, params=genTokenPayload, verify=True)

    # If the response back is 200:
    if(genTokenPost.ok):

        # Token response json
        genTokenData = json.loads(genTokenPost.content)
        # Gets the token from the json
        genToken = genTokenData['token']

        return genToken

    # If response is not 200, raise error
    else:
        genTokenPost.raise_for_status()


def add_app_via_rest(env, user, password, number):
    """Adds new application via ArcGIS Online Rest API.
    Uses http://www.python-requests.org/en/latest/
    for making the requests"""

    url = env_switcher(env)[0]

    # Build the url
    addAppUrl = url + '/sharing/rest/content/users/' + user + '/addItem'

    # Get a new token
    genToken = gen_token_via_rest(url, user, password)

    # Create the amount of apps desired by number
    for i in range(number):

        # Make up a new name by appending a random numbers
        test_name = 'test' + str(random())

        def randostring(length):
            """Generates random string to create unique tag"""

            return(''.join([choice(ascii_letters + digits) for n in range(length)]))
        test_tags = randostring(5)

        # Query string parameters
        addAppPayload = {
            'f': 'json',
            'token': genToken,
            'title': test_name,
            'type': 'Web Mapping Application',
            'tags': test_tags
        }

        # Make the call to the endpoint with parameters
        addAppPost = requests.post(
            addAppUrl, params=addAppPayload, verify=True)

        # Get the response as a variable
        addAppData = json.loads(addAppPost.content)

    # Return the ID of the newly created application
    return [addAppData['id'], test_name, test_tags, addAppPayload]


def add_layer_via_rest(env, user, password, number):
    """Adds new layer via ArcGIS Online Rest API.
    Uses http://www.python-requests.org/en/latest/
    for making the requests"""

    # Get the base url
    url = env_switcher(env)[0]

    # Get a new token
    gen_token = gen_token_via_rest(url, user, password)

    # Build the url
    add_layer_url = url + '/sharing/rest/content/users/' + user + '/createService'

    # Create the amount of apps desired by number
    for i in range(number):

        # Make up a new name by appending a random numbers
        test_name = 'test' + str(random())

        # Creates a random string for make unique tags, names, etc
        def randostring(length):
            """Generates random string to create unique tag"""

            return(''.join([choice(ascii_letters + digits) for n in range(length)]))

        # Create a unique tag
        test_tags = randostring(5)

        # JSON definition to create the layer
        add_layer_definition = {
            "name": test_name,
            "serviceDescription": "",
            "hasStaticData": "false",
            "maxRecordCount": 1000,
            "supportedQueryFormats": "JSON",
            "capabilities": "Create,Delete,Query,Update,Editing",
            "description": "",
            "copyrightText": "",
            "spatialReference": {
                "wkid": 102100
            },
            "initialExtent": {
                "xmin": -20037507.0671618,
                "ymin": -30240971.9583862,
                "xmax": 20037507.0671618,
                "ymax": 18398924.324645,
                "spatialReference": {
                    "wkid": 102100,
                    "latestWkid": 3857
                }
            },
            "allowGeometryUpdates": "true",
            "units": "esriMeters",
            "xssPreventionInfo": {
                "xssPreventionEnabled": "true",
                "xssPreventionRule": "InputOnly",
                "xssInputRule": "rejectInvalid"
            }
        }

        # Query string parameters
        add_layer_payload = {
            'f': 'json',
            'token': gen_token,
            'createParameters': json.dumps(add_layer_definition)
        }

        # Make the call to the endpoint with parameters
        add_layer_post = requests.post(
            add_layer_url, data=add_layer_payload, verify=True)

        # Get the response as a object
        add_layer_data = add_layer_post.json()

        # Get the returned layer's item ID
        layer_id = add_layer_data['itemId']

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ update item ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # URL for updating the layer information
        update_item_url = url + '/sharing/rest/content/users/' + \
            user + '/items/' + str(layer_id) + '/update'

        # Query string parameters
        update_item_payload = {
            'f': 'json',
            'token': gen_token,
            'tags': test_tags
        }

        # Make the call to the endpoint with parameters
        requests.post(update_item_url, data=update_item_payload, verify=True)

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ add to definition ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        # Service URL returned in the first call
        original_encoded_service_url = add_layer_data['encodedServiceURL']

        # Updates the URL for the next call
        admin_encoded_service_url = original_encoded_service_url.replace(
            '/rest/services/', '/rest/admin/services/')

        # URL for updating layer's definition
        add_to_definition_url = admin_encoded_service_url + '/addToDefinition'

        # JSON definition to add to the layer definition
        add_to_definition_definition = {
            "layers": [
                {
                    "adminLayerInfo": {
                        "tableName": "db_10.user_10.LOADTESTSOIL_LOADTESTSOIL",
                        "geometryField": {
                            "name": "Shape"
                        },
                        "xssTrustedFields": ""
                    },
                    "id": 0,
                    "name": "LoadTestSoil",
                    "type": "Feature Layer",
                    "displayField": "",
                    "description": "",
                    "copyrightText": "",
                    "defaultVisibility": "true",
                    "ownershipBasedAccessControlForFeatures": {
                        "allowOthersToQuery": "false",
                        "allowOthersToDelete": "false",
                        "allowOthersToUpdate": "false"
                    }
                }
            ]
        }

        # Query string parameters
        add_to_definition_payload = {
            'f': 'json',
            'token': gen_token,
            'addToDefinition': json.dumps(add_to_definition_definition)
        }

        # Make the call to the endpoint with parameters and definition
        requests.post(add_to_definition_url,
                      data=add_to_definition_payload, verify=True)

    # Return the ID of the newly created application
    return [layer_id, test_name, test_tags]


def delete_item_via_rest(env, user, password, itemId):
    """Deletes any passed item from ArcGIS Online via ArcGIS Online Rest API.
    If a layer has a related item such as a file which created it, that
    will be delete, too. Uses http://www.python-requests.org/en/latest/
    for making the requests"""

    url = env_switcher(env)[0]

    # Get a new token
    genToken = gen_token_via_rest(url, user, password)

    # Build url
    relationUrl = url + '/sharing/rest/content/items/' + itemId + '/relatedItems'

    # Needed query string params to be added to the URL
    relationPayload = {
        'relationshipType': 'Service2Data',
        'direction': 'forward',
        'f': 'json',
        'token': genToken
    }

    # Related items post call with appended params
    relationPost = requests.post(
        relationUrl, params=relationPayload, verify=True)
    # Related call return json

    relationData = json.loads(relationPost.content)

    # If a related item is found ...
    if relationData['total'] == 1:

        # Set variables for the items to be deleted
        itemOne = itemId
        itemTwo = relationData['relatedItems'][0]['id']

        # URL for deleting multiple items
        delAllUrl = url + '/sharing/rest/content/users/' + user + '/deleteItems'

        # Needed query string params to be added to the URL
        delAllPayload = {
            'items': itemOne + ',' + itemTwo,
            'f': 'json',
            'token': genToken}

        # Makes post call and appends params
        delAllPost = requests.post(
            delAllUrl, params=delAllPayload, verify=True)

        # Delete all items json response
        delAllData = json.loads(delAllPost.content)

        # Get success message for each item
        sucMsgOne = delAllData['results'][0]['success']
        sucMsgTwo = delAllData['results'][1]['success']

        # Check that items were deleted properly and return message
        if sucMsgOne and sucMsgTwo is True:
            print('Both items successfully deleted upon test completion')
        else:
            print('An error occurred while deleting items')

    # Continues process for deleting single item if no related item is found
    else:
        # # URL for deleting single item
        delUrl = url + '/sharing/rest/content/users/' + \
            user + '/items/' + itemId + '/delete'

        # Needed query string params to be added to the URL
        delPayload = {'f': 'json', 'token': genToken}

        # Makes post call and appends params
        delPost = requests.post(delUrl, params=delPayload, verify=True)

        # Delete single item json response
        delData = json.loads(delPost.content)

        # Get success message for item
        sucMsg = delData['success']

        # Check that item was deleted properly and return message
        if sucMsg is True:
            print('Item successfully deleted upon test completion')
        else:
            print('An error occurred while deleting item')


def delete_single_item_via_rest(env, user, password, itemId):
    """Deletes only a single item at a time"""

    url = env_switcher(env)[0]

    # Get a new token
    genToken = gen_token_via_rest(url, user, password)
    
    # URL for deleting single item
    delUrl = url + '/sharing/rest/content/users/' + \
        user + '/items/' + itemId + '/delete'

    # Needed query string params to be added to the URL
    delPayload = {'f': 'json', 'token': genToken}

    # Makes post call and appends params
    delPost = requests.post(delUrl, params=delPayload, verify=True)

    # Delete single item json response
    delData = json.loads(delPost.content)

    # Get success message for item
    sucMsg = delData['success']

    # Check that item was deleted properly and return message
    if sucMsg is True:
        print('Item successfully deleted before test start')
    else:
        print('An error occurred while deleting item')

def get_item_info_via_rest(env, user, password, itemId):
    """Gets single item information via rest endpoint"""

    url = env_switcher(env)[0]

    # Get a new token
    genToken = gen_token_via_rest(url, user, password)
    
    # URL for deleting single item
    layer_info_url = url + '/sharing/rest/content/items/' + itemId

    # Needed query string params to be added to the URL
    layer_info_payload = {'f': 'json', 'token': genToken}

    # Makes post call and appends params
    layer_info_post = requests.post(layer_info_url, params=layer_info_payload, verify=True)

    # Delete single item json response
    layer_info_data = json.loads(layer_info_post.content)

    return(layer_info_data)


def get_available_credits(env, user, password):
    """"Gets the available credits for a given user"""

    url = env_switcher(env)[0]

    # Generate a token for the user
    genToken = gen_token_via_rest(url, user, password)

    # Build URL from passed environment and URI for endpoint
    availableCreditsUrl = url + '/sharing/rest/portals/self'

    # Parameters for call
    availableCreditsPayload = {
        'f': 'json',
        'token': genToken
    }

    # Make the post to the api
    availableCreditsPost = requests.post(
        availableCreditsUrl, params=availableCreditsPayload, verify=True)

    # Returned data from call
    availableCreditsData = json.loads(availableCreditsPost.content)

    # Return the available credits
    return availableCreditsData['subscriptionInfo']['availableCredits']


def get_total_credits(env, user, password):

    url1 = env_switcher(env)[0]
    url2 = env_switcher(env)[1]

    # Generate a token for the user
    genToken = gen_token_via_rest(url1, user, password)

    # Build URL from passed environment and URI for endpoint
    totalCreditsUrl = url2 + '/sms/rest/subscription/developers/subscriptionInfo'

    # Parameters for call
    totalCreditsPayload = {
        'token': genToken
    }

    # Make the post to the api
    totalCreditsPost = requests.get(
        totalCreditsUrl, params=totalCreditsPayload, verify=True)

    # Returned data from call
    totalCreditsData = json.loads(totalCreditsPost.content)

    # Possible know membership levels
    levels = {
        None: '50.00',
        'Level 1': '200.00',
        'Level 2': '900.00',
        'Level 3': '2000.00',
        'Level 4': '4000.00',
        'Level 5': '10000.00',
        'Level 6': '20000.00',
        'Level 7': '40000.00'
    }

    # Figure the Level from known credits
    for i in range(len(dig(totalCreditsData, 'subscriptions'))):
        if dig(totalCreditsData, 'subscriptions', i, 'subscriptionSubType') in levels:
            return levels[dig(totalCreditsData, 'subscriptions', i, 'subscriptionSubType')]


def search_query(env, user, password, file_name):
    """Uses the search API to locate and delete any
    passed file or title name passed in from any user."""

    url = env_switcher(env)[0]

    # Generate a token for the user
    genToken = gen_token_via_rest(url, user, password)

    # Build URL from passed environment and URI for endpoint
    searchQueryURL = url + '/sharing/rest/search'

    # Parameters for call
    searchQueryPayload = {
        'f': 'json',
        'q': file_name + ' owner:' + user,
        'token': genToken
    }

    # Make the post to the api
    searchQueryPost = requests.post(
        searchQueryURL, params=searchQueryPayload, verify=True)

    # Returned data from call
    searchQueryData = json.loads(searchQueryPost.content)

    # If a featured layer or file with this name exist, remove them
    if len(searchQueryData['results']) > 0:
        for result in searchQueryData['results']:
            delete_single_item_via_rest(env,
                                        user,
                                        password,
                                        result['id'],
                                        genToken)
