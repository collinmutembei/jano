import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

interface JournalState {
  journals: Array<{ id: number; title: string; content: string; category: string }>;
  loading: boolean;
  error: string | null;
}

const initialState: JournalState = {
  journals: [],
  loading: false,
  error: null,
};

export const fetchJournals = createAsyncThunk(
  'journal/fetchJournals',
  async (_, { rejectWithValue }) => {
    try {
      const token = await AsyncStorage.getItem('token');
      const response = await axios.get(`${API_URL}/journal`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const createJournal = createAsyncThunk(
  'journal/createJournal',
  async (journalData: { title: string; content: string; category: string }, { rejectWithValue }) => {
    try {
      const token = await AsyncStorage.getItem('token');
      const response = await axios.post(`${API_URL}/journal`, journalData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

// export const fetchJournal = createAsyncThunk(
//   'journal/fetchJournal',
//   async ({ id }: {id: number}, { rejectWithValue }) => {
//     try {
//       const token = await AsyncStorage.getItem('token');
//       const response = await axios.get(`${API_URL}/journal/${id}`, {
//         headers: { Authorization: `Bearer ${token}` },
//       });
//       return response.data;
//     } catch (error) {
//       return rejectWithValue(error.response.data);
//     }
//   }
// );

export const updateJournal = createAsyncThunk(
  'journal/updateJournal',
  async ({ id, journalData }: { id: number; journalData: { title: string; content: string; category: string } }, { rejectWithValue }) => {
    console.log("id", id)
    console.log("journalData", journalData)
    try {
      const token = await AsyncStorage.getItem('token');
      const response = await axios.put(`${API_URL}/journal/${id}`, journalData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const deleteJournal = createAsyncThunk(
  'journal/deleteJournal',
  async (id: number, { rejectWithValue }) => {
    try {
      const token = await AsyncStorage.getItem('token');
      const response = await axios.delete(`${API_URL}/journal/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return { id };
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

const journalSlice = createSlice({
  name: 'journal',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchJournals.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchJournals.fulfilled, (state, action) => {
        state.journals = action.payload;
        state.loading = false;
      })
      .addCase(fetchJournals.rejected, (state, action) => {
        state.error = action.payload as string;
        state.loading = false;
      })
      .addCase(createJournal.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createJournal.fulfilled, (state, action) => {
        state.journals.push(action.payload);
        state.loading = false;
      })
      .addCase(createJournal.rejected, (state, action) => {
        state.error = action.payload as string;
        state.loading = false;
      })
      .addCase(updateJournal.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateJournal.fulfilled, (state, action) => {
        const index = state.journals.findIndex(journal => journal.id === action.payload.id);
        if (index !== -1) {
          state.journals[index] = action.payload;
        }
        state.loading = false;
      })
      .addCase(updateJournal.rejected, (state, action) => {
        state.error = action.payload as string;
        state.loading = false;
      })
      .addCase(deleteJournal.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(deleteJournal.fulfilled, (state, action) => {
        state.journals = state.journals.filter(journal => journal.id !== action.payload.id);
        state.loading = false;
      })
      .addCase(deleteJournal.rejected, (state, action) => {
        state.error = action.payload as string;
        state.loading = false;
      });
  },
});

export default journalSlice.reducer;
