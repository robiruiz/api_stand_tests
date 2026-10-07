import sender_stand_request
import data


# Esta función cambia el valor del parámetro "firstName"
def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


# Función de prueba positiva
def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1


# Función de prueba negativa para símbolos, longitud, números, etc.
def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == \
        "Has introducido un nombre de usuario no válido. " \
        "El nombre solo puede contener letras del alfabeto latino, " \
        "la longitud debe ser de 2 a 15 caracteres."


# Función de prueba negativa para los casos sin firstName válido
def negative_assert_no_firstname(user_body):
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == \
        "No se han aprobado todos los parámetros requeridos"


# Prueba 1. El parámetro "firstName" contiene 2 caracteres
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")


# Prueba 2. El parámetro "firstName" contiene 15 caracteres
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")


# Prueba 3. El parámetro "firstName" contiene 1 carácter
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")


# Prueba 4. El parámetro "firstName" contiene 16 caracteres
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")


# Prueba 5. El parámetro "firstName" contiene un espacio
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A Aaa")


# Prueba 6. El parámetro "firstName" contiene caracteres especiales
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")


# Prueba 7. El parámetro "firstName" contiene números
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")


# Prueba 8. Error
# La solicitud no contiene el parámetro "firstName"
def test_create_user_no_first_name_get_error_response():
    # El diccionario con el cuerpo de la solicitud se copia del archivo "data" a la variable "user_body"
    # De lo contrario, se podrían perder los datos del diccionario de origen
    user_body = data.user_body.copy()

    # El parámetro "firstName" se elimina de la solicitud
    user_body.pop("firstName")

    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)


# Prueba 9. Error
# El parámetro "firstName" contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body("")

    # Comprueba la respuesta
    negative_assert_no_firstname(user_body)


# Prueba 10. Error
# El parámetro "firstName" contiene un número en lugar de un string
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400