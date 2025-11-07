# Diccionario de equivalencias UDS -> SAE
uds_to_sae = {
    '0': 'P0', '1': 'P1', '2': 'P2', '3': 'P3',
    '4': 'C0', '5': 'C1', '6': 'C2', '7': 'C3',
    '8': 'B0', '9': 'B1', 'A': 'B2', 'B': 'B3',
    'C': 'U0', 'D': 'U1', 'E': 'U2', 'F': 'U3'
}

uds_list = [
"0xD80886","0xC40182","0x940105","0xC00008","0x905200",
"0x575000","0x960A87","0x92239A","0xDA1487","0x940020",
"0x9C10DD","0x9C40B0","0xD61401","0x962394","0xD66DF0",
"0xC10000","0x58040A","0x940014","0x940010","0xD80C87",
"0xD80087","0x1900F2","0x940246","0xD81887","0x940266",
"0x92A486","0x540700","0x9A6029"
]


def uds_to_sae_convert_list(uds_list):
    result = []
    for val in uds_list:
        if val.startswith("0x"):
            first_digit = val[2].upper()  # Primer dígito después de '0x'
            sae_prefix = uds_to_sae.get(first_digit, '?')
            rest = val[3:]  # El resto del valor
            result.append(f"{sae_prefix}{rest}")
        else:
            result.append("Formato inválido")
    return result

def uds_to_sae_convert(uds):
    result=''
    if uds.startswith("0x"):
        first_digit = uds[2].upper()  # Primer dígito después de '0x'
        sae_prefix = uds_to_sae.get(first_digit, '?')
        rest = uds[3:]  # El resto del valor
        result=f"{sae_prefix}{rest}"
    else:
        result.append("Formato inválido")
    return result


# print("UDS -> SAE:", uds_to_sae_convert(uds_list))
