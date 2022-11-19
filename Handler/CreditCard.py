from flask import jsonify
from DAO.CreditCard import CreditCardDao

class CreditCardHandler:


    def build_credit_cards_dict(self, row):
        result = {}
        result['cardid'] = row[0]
        result['fname'] = row[1]
        result['lname'] = row[2]
        result['cexpdate'] = row[3]
        result['cvv'] = row[4]
        result['cardnum'] = row[5]
        result['user_id'] = row[6]
        return result


    def getAllUsersCreditCards(self):
        dao = CreditCardDao()
        card_list = dao.getAllUsersCreditCards()
        result_list = []
        for row in card_list:
            result = self.build_credit_cards_dict(row)
            result_list.append(result)
        return jsonify(CreditCards=result_list)

