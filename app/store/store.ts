import { configureStore } from '@reduxjs/toolkit';
import journalReducer from './journal';
import authReducer from './auth';

const store = configureStore({
  reducer: {
    journal: journalReducer,
    auth: authReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export default store;
