import React, { useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { fetchJournals } from '../store/journal';
import { RootState } from '../store/store';
import { useNavigation } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';

const HomeScreen = () => {
  const dispatch = useDispatch();
  const navigation = useNavigation();
  const journals = useSelector((state: RootState) => state.journal.journals);
  console.log(journals)

  useEffect(() => {
    dispatch(fetchJournals());
  }, [dispatch]);

  const renderItem = ({ item }: any) => (
    <TouchableOpacity
      style={styles.journalItem}
      onPress={() => navigation.navigate('JournalDetail', { journal: item })}
    >
      <Text style={styles.journalTitle}>{item.title}</Text>
      <Text style={styles.journalCategory}>{item.category}</Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.addButton}
          onPress={() => navigation.navigate('AddJournal')}
        >
          <Text style={styles.addButtonText}>Add Journal</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.menuButton}
          onPress={() => navigation.navigate('Settings')}
        >
          <Ionicons name="settings" size={24} color="white" />
        </TouchableOpacity>
      </View>
      <FlatList
        data={journals}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 10,
  },
  addButton: {
    backgroundColor: '#6200ee',
    padding: 10,
    borderRadius: 5,
  },
  addButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
  menuButton: {
    backgroundColor: '#6200ee',
    padding: 10,
    borderRadius: 5,
  },
  listContainer: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  journalItem: {
    backgroundColor: '#f9f9f9',
    padding: 20,
    marginVertical: 10,
    // minWidth: "500px",
    width: '500px',
    borderRadius: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
  },
  journalTitle: {
    overflow: 'hidden',
    whiteSpace: 'no-wrap',
    textOverflow: 'ellipsis',
    fontSize: 16,
    fontWeight: 'bold',
  },
  journalCategory: {
    fontSize: 14,
    color: 'gray',
  },
});

export default HomeScreen;
