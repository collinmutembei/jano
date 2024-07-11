import React, { useState } from 'react';
import { View, TextInput, Button, StyleSheet } from 'react-native';
import { useDispatch } from 'react-redux';
import { updateJournal } from '../store/journal';
import { useNavigation, useRoute } from '@react-navigation/native';

const JournalDetailScreen = () => {
  const route = useRoute();
  const navigation = useNavigation();
  const { journal } = route.params
  console.log("journal", journal)
  const [title, setTitle] = useState(journal.title);
  const [content, setContent] = useState(journal.content);
  const [category, setCategory] = useState(journal.category);
  const dispatch = useDispatch();

  const handleUpdateJournal = () => {
    dispatch(updateJournal({ ...journal, title, content, category }));
    navigation.goBack();
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Title"
        value={title}
        onChangeText={setTitle}
      />
      <TextInput
        style={styles.input}
        placeholder="Content"
        value={content}
        onChangeText={setContent}
      />
      <TextInput
        style={styles.input}
        placeholder="Category"
        value={category}
        onChangeText={setCategory}
      />
      <Button title="Update Journal" onPress={handleUpdateJournal} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  input: {
    width: '100%',
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 20,
    paddingHorizontal: 10,
  },
});

export default JournalDetailScreen;
