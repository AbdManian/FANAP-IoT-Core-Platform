# Check if user if owner of this deviceid or there is a role
# For accessing this device type for the user
#
#
# 1 D Check if user has access to the target device
# 2   Validate attributes based on the devicetype
# 3   Validate fields based on


from app.device import get_by_deviceid_or_404
from app.validation import devicedata_validator
from app.exception import ApiExp

import app.devicetype
from app.role import role_get_device_permission_dict


def convert_attribute_list_to_dict(attribute_list):
    return {x['name']: x['value'] for x in attribute_list}


def validate_data_metadatafileds(fileds, user_data_dict):
    for fname in user_data_dict.keys():
        if fname not in fileds:
            raise ApiExp.Structural(
                dbg_msg='Can not send/write data for "{}"'.format(fname))


def check_user_write_field_access(user, device, user_field_list):
    pl = role_get_device_permission_dict(user, device)
    if not pl.check_write_access(user_field_list):
        raise ApiExp.AccessDenied(
            dbg_msg='No access for read/write device field')
    return True


def write_send_common_validate(user, data, deviceid, params, is_write):
    # Check if any device is assigned to this user:
    device = get_by_deviceid_or_404(user, deviceid, look_in_granted=True)

    devicetype = device.devicetype

    user_data_dict = convert_attribute_list_to_dict(data['attributes'])

    # Validate user request body based on device-type
    devicedata_validator(devicetype.attributes, user_data_dict)

    data_fileds, metadata_fields = app.devicetype.get_devicefields_metadata(
        devicetype)

    validate_data_metadatafileds(
        metadata_fields if is_write else data_fileds,
        user_data_dict)

    check_user_write_field_access(user, device, user_data_dict.keys())

    return dict(msg='This is device data write',
                dname=device.name,
                dtname=devicetype.name,
                data=user_data_dict,
                data_fileds=data_fileds,
                metadata_fields=metadata_fields,
                )


def devicedata_write(user, data, deviceid, params):
    return write_send_common_validate(
        user, data, deviceid, params, is_write=True
    )


def devicedata_read(user, deviceid, params):
    # Check if any device is assigned to this user:
    device = get_by_deviceid_or_404(user, deviceid, look_in_granted=True)

    return dict(msg='This is device data read', deviceid=deviceid)


def devicedata_send(user, data, deviceid, params):
    return write_send_common_validate(
        user, data, deviceid, params, is_write=False
    )