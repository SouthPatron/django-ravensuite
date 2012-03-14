""" Views common to all applications

These views are used throughout the packages and they
inherently support RESTful access (CRUD). The CRUD mappings are
as follows:

	Create - POST
	Read - GET
	Update - PUT
	Delete - DELETE

They support multiple request and response formats. The currently
supported formats are:

	HTML
	JSON

Available classes:

	. ListView	- Display a list of objects
	. SingleObjectView - Display a single object
	. ModalView - Retrieve a particular modal from the
		system for display purposes on a page.

"""

