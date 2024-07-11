import React from 'react';
import { createStackNavigator } from '@react-navigation/stack';
// import { createDrawerNavigator } from '@react-navigation/drawer';
import { NavigationContainer } from '@react-navigation/native';

import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';
import HomeScreen from '../screens/HomeScreen';
import JournalDetailScreen from '../screens/JournalDetailScreen';
import AddJournalScreen from '../screens/AddJournalScreen';
import SettingsScreen from '../screens/SettingsScreen';

const Stack = createStackNavigator();
// const Drawer = createDrawerNavigator();

const AuthStack = () => (
  <Stack.Navigator>
    <Stack.Screen name="Login" component={LoginScreen} />
    <Stack.Screen name="Register" component={RegisterScreen} />
  </Stack.Navigator>
);

const HomeStack = () => (
  <Stack.Navigator>
    <Stack.Screen name="Jano" component={HomeScreen} />
    <Stack.Screen name="JournalDetail" component={JournalDetailScreen} />
    <Stack.Screen name="AddJournal" component={AddJournalScreen} />
    <Stack.Screen name="Settings" component={SettingsScreen} />
  </Stack.Navigator>
);

// const AppDrawer = () => (
//   <Drawer.Navigator>
//     <Drawer.Screen name="Home" component={HomeStack} />
//     <Drawer.Screen name="Settings" component={SettingsScreen} />
//   </Drawer.Navigator>
// );

const MainNavigator = ({ isAuthenticated }: { isAuthenticated: boolean }) => {
  return (
    <NavigationContainer>
      {isAuthenticated ? <HomeStack /> : <AuthStack />}
    </NavigationContainer>
  );
};

export default MainNavigator;
