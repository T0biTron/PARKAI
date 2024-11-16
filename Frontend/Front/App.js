import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import SplashScreen from './app/Components/SplashScreen';
import LoginScreen from './app/Components/LoginScreen';
import RegisterScreen from './app/Components/RegisterScreen';
import BuscarEspacios from './app/Components/BuscarEspacios';
import HistorialReservas from './app/Components/HistorialReservas';

const Stack = createStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Splash">
        <Stack.Screen
          name="Splash"
          component={SplashScreen}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="Login"
          component={LoginScreen}
          options={{ title: 'Iniciar Sesión' }}
        />
        <Stack.Screen
          name="Register"
          component={RegisterScreen}
          options={{ title: 'Registro' }}
        />
        <Stack.Screen
          name="BuscarEspacios"
          component={BuscarEspacios}
          options={{ title: 'Buscar Espacios' }}
        />
        <Stack.Screen
          name="HistorialReservas"
          component={HistorialReservas}
          options={{ title: 'Historial de Reservas' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}
