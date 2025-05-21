import requests

def test_user(baseurl,header):
	url = baseurl + '/ckm/rest/v1/archetypes'
	response = requests.get(url, headers=header)
	code = response.status_code

	if code != 200:
		print('Authorization failed. Downloading public data.')
		return False
	else:
		print('User authorization successful!')
		return True



def main():
	from base64 import b64encode

	def basic_auth(username, password):
		token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
		return f'Basic {token}'
	baseurl = 'https://ckm.salut.gencat.cat'
	user = ''
	pw = ''

	header = { 'Authorization' : basic_auth(user, pw) }

	test_user(baseurl,header)

if __name__=="__main__":
	main()
