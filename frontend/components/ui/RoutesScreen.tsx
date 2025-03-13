import React, { useState } from "react";
import {
  View,
  TextInput,
  TouchableOpacity,
  Text,
  StyleSheet,
  ToastAndroid,
} from "react-native";
import { Picker } from "@react-native-picker/picker";
import { StackNavigationProp } from "@react-navigation/stack";
import { RootStackParamList } from "../types";
import { DOMAIN_URL, Messages, Headers, ReqRespKey } from "../util/Constant";

type RegisterScreenNavigationProp = StackNavigationProp<
  RootStackParamList,
  "Register"
>;

type Props = {
  navigation: RegisterScreenNavigationProp;
};
type Props = {
  navigation: RegisterScreenNavigationProp;
};

const RegisterScreen: React.FC<Props> = ({ navigation }) => {
  const [usernameAvailable, setUsernameAvailable] = useState<boolean>(false);
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState("");
  const [foreigner, setForeigner] = useState("0"); // Default value is local user
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState<string>("");

  const handleUsernameAvailable = async (username: string) => {
    try {
      if (username.length <= 5) {
        setErrorMessage("Username length should be more than 5");
        setSuccessMessage("");
      } else {
        const response = await fetch(
          `${DOMAIN_URL}/username-available?username=${username}`,
          {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        const data = await response.json();

        if (data.available) {
          setUsernameAvailable(true);
          setSuccessMessage("Username is available");
          setErrorMessage("");
        } else {
          setUsernameAvailable(false);
          setErrorMessage("Username is taken");
          setSuccessMessage("");
        }
      }
    } catch (error) {
      setErrorMessage("Failed to connect to the server");
    }
  };

  const handleRegister = async () => {
    if (!username || !password) {
      setErrorMessage("Please enter a valid username and password");
    } else {
      setErrorMessage("");
      try {
        if (username.length <= 5) {
          setErrorMessage("Username length should be more than 5");
        } else {
          if (usernameAvailable == true) {
            const response = await fetch(`${DOMAIN_URL}/register`, {
              method: "POST",
              headers: Headers.JSON,
              body: JSON.stringify({ username, password, foreigner }),
            });

            const responseBody = await response.json();

            if (response.ok) {
              const message = responseBody[ReqRespKey.MESSAGE_REQUEST];
              if (message === Messages.REGISTER_SUCCESS_MESSAGE) {
                ToastAndroid.show(
                  Messages.REGISTER_SUCCESS_MESSAGE,
                  ToastAndroid.SHORT
                );
                navigation.navigate("Dashboard");
              } else {
                setErrorMessage(Messages.SOMETHING_WRONG_MESSAGE);
              }
            } else {
              const message = responseBody[ReqRespKey.MESSAGE_REQUEST];
              setErrorMessage(message || Messages.SOMETHING_WRONG_MESSAGE);
            }
          } else {
            setErrorMessage("Username is taken");
          }
        }
      } catch (error) {
        setErrorMessage(Messages.FAILED_TO_CONNECT_MESSAGE);
      }
    }
  };

  return (
    <View style={styles.container}>
      {/* Username Input */}
      <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={(text: string) => {
          setUsername(text);
          handleUsernameAvailable(text);
        }}
        placeholderTextColor="#757575"
      />

      {/* Password Input */}
      <TextInput
        style={styles.input}
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry={true}
        placeholderTextColor="#757575"
      />

      {/* Foreigner/Local User Selector */}
      <Picker
        selectedValue={foreigner}
        onValueChange={(itemValue) => setForeigner(itemValue)}
        style={styles.picker}
      >
        <Picker.Item label="Local User" value="0" />
        <Picker.Item label="Foreign User" value="1" />
      </Picker>

      {/* Register Button */}
      <TouchableOpacity style={styles.button} onPress={handleRegister}>
        <Text style={styles.buttonText}>REGISTER</Text>
      </TouchableOpacity>

      {/* Error Message */}
      {errorMessage ? (
        <Text style={styles.errorMessage}>{errorMessage}</Text>
      ) : null}

      {/* Success Message */}
      {successMessage ? (
        <Text style={styles.successMessage}>{successMessage}</Text>
      ) : null}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    backgroundColor: "#57585b",
    paddingHorizontal: 20,
  },
  input: {
    backgroundColor: "#FFFFFF",
    padding: 12,
    marginVertical: 10,
    borderRadius: 8,
    fontSize: 16,
    color: "#000000",
  },
  picker: {
    backgroundColor: "#FFFFFF",
    marginVertical: 10,
    borderRadius: 8,
    fontSize: 16,
    color: "#000000",
  },
  errorMessage: {
    color: "#FF0000",
    marginTop: 10,
    textAlign: "center",
    backgroundColor: "#FFCCCC",
    padding: 10,
    borderRadius: 8,
  },
  successMessage: {
    color: "#00FF00",
    marginTop: 10,
    textAlign: "center",
    backgroundColor: "#CCFFCC",
    padding: 10,
    borderRadius: 8,
  },
  button: {
    width: "100%",
    marginTop: 10,
    backgroundColor: "#007AFF",
    padding: 15,
    borderRadius: 30,
    alignItems: "center",
  },
  buttonText: {
    color: "#FFFFFF",
    fontSize: 16,
  },
});

export default RegisterScreen;
