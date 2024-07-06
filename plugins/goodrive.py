import gspread
from oauth2client.service_account import ServiceAccountCredentials

class Sheet:

	def __init__(self, cred_filename:str):
		scope = ['https://spreadsheets.google.com/feeds']
		creds = ServiceAccountCredentials.from_json_keyfile_name(cred_filename, scope)
		client = gspread.authorize(creds)
		self._sheet = client.open_by_key('1CZ0A8LTy5OoG4Y7OD9IF0efszTizte55LBEsP3ELsSU').sheet1 # https://docs.google.com/spreadsheets/d/1CZ0A8LTy5OoG4Y7OD9IF0efszTizte55LBEsP3ELsSU/edit?gid=0#gid=0


	def update_cell(self, cell:str, data:str) -> None:
		self._sheet.update_acell(cell, data)

	def read_cell(self, cell:str) -> str:
		return self._sheet.cell(ord(cell[0])-64, int(cell[1])).value