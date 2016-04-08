# @author Tobias Krauthoff
# @email krauthoff@cs.uni-duesseldorf.de


class Validator:

	@staticmethod
	def do_something():
		return 1

	@staticmethod
	def save_params_in_session(session, user_arg_uid, sys_arg_uid, mood, reaction):
		session['user_arg_uid'] = user_arg_uid
		session['sys_arg_uid'] = sys_arg_uid
		session['mood'] = mood
		session['reaction'] = reaction

	@staticmethod
	def validate_params_with_session(session, user_arg_uid, sys_arg_uid, mood, reaction):
		"""

		:param session:
		:param user_arg_uid:
		:param sys_arg_uid:
		:param mood:
		:param reaction:
		:return:
		"""
		if session['user_arg_uid'] != user_arg_uid:
			return 1
		if session['sys_arg_uid'] != sys_arg_uid:
			return 2
		if session['mood'] != mood:
			return 3
		if session['reaction'] != reaction:
			return 4
		return 0
