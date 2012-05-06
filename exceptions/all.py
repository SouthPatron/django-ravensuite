


class BLE_Error( Exception ):
	pass



class BLE_DevError( BLE_Error ):
	pass

class BLE_ConflictError( BLE_Error ):
	pass

class BLE_NotFoundError( BLE_Error ):
	pass

class BLE_ProcessFlowError( BLE_Error ):
	pass

class BLE_ValueRangeError( BLE_Error ):
	pass

class BLE_InvalidInputError( BLE_Error ):
	pass

