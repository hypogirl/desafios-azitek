import { createStore } from 'vuex';
import localStoragePlugin from '/plugins/localStorage';

export default createStore({
    state: {
      todos: []
    },
    getters: {
        favorites: state => state.todos.filter(todo => todo.favorite)
    },
    mutations: {
        addTodo(state, todo) {
        state.todos.push(todo);
        },
        editTodo(state, newTodo) {
            state.todos[newTodo["index"]].title = newTodo["title"]
            state.todos[newTodo["index"]].description = newTodo["description"]
            state.todos[newTodo["index"]].favorite = newTodo["favorite"]
            state.todos[newTodo["index"]].id = newTodo["id"]

        },
        deleteTodo(state, index) {
            state.todos.splice(index, 1);
        },
        addToFavorites(state, index) {
            state.todos[index].favorite = true
        },
        removeFromFavorites(state, index) {
            state.todos[index].favorite = false
        },
    },
    actions: {
    },
    modules: {
    },
    plugins: [localStoragePlugin],
})