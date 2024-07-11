import React, { useEffect } from 'react';
import { Provider, useDispatch, useSelector } from 'react-redux';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { checkAuth } from './store/auth';
import MainNavigator from './navigation/MainNavigator';
import store, { RootState } from './store/store';
import Toast from 'react-native-toast-message';


const AppNavigator = () => {
  const dispatch = useDispatch();
  const isAuthenticated = useSelector((state: RootState) => !!state.auth.user);

  useEffect(() => {
    dispatch(checkAuth());
  }, [dispatch]);

  return <MainNavigator isAuthenticated={isAuthenticated} />;
};

const App = () => {
  return (
    <Provider store={store}>
      <SafeAreaProvider>
        <AppNavigator />
        <Toast ref={(ref) => Toast.setRef(ref)} />
      </SafeAreaProvider>
    </Provider>
  );
};

export default App;
