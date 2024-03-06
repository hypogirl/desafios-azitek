<template>
    <div class="new-todo">
        <div class="normal-todo">
            <h2>Adicionar novo to do</h2>
            <input v-model="newTodo.title" placeholder="Título" class="big-title margin-block" required />
            <textarea v-model="newTodo.description" placeholder="Descrição" class="margin-block" style="white-space: pre-line;" required></textarea>
            <button id="new-todo" class="orange-button margin-block" @click="addTodo">Adicionar</button>
        </div>
        <div class="cat-todo">
            <h2>Adicionar to do's com factos sobre gatos</h2>
            <input type="number" v-model="numberOfFacts" placeholder="Número de factos" class="big-title margin-block" style="width: 45%; display: inline;" required />
            <button id="new-cat" class="orange-button margin-block" @click="createFacts()">Adicionar</button>
        </div>
    </div>
  
    <ul class="todo-list">
        <li><h2 class="titles">Lista de to do's</h2></li>
        <li>
            <div class="filters">
                <div class="filter-div"><h3>Filtrar por título:</h3><input v-model="filterTitle" /></div>
                <div class="filter-div"><h3>Filtrar por descrição:</h3><input v-model="filterDescription" /></div>
            </div>
        </li>
        <li class="todos">
            <li class="todo-body" :id="'todo-'+todo.id" v-for="(todo, index) in filteredTodos" :key="index">
                <div class="todo-top">
                    <h1 class="main-title">{{ fixTitleLength(todo.title, 40) }}</h1>
                    <input v-model="editingTodo.title" placeholder="Novo título" value="${todo.title}" class="title-change big-title margin-block" required style="display: none;"/>
                    <button class="edit orange-button" @click="editTodo(todo.id)">Editar</button>
                    <button class="confirm orange-button" @click="confirmEdit(todo.id)" style="display: none;">Confirmar</button>
                    <button class="cancel orange-button" @click="cancelEdit(todo.id)" style="display: none;">Cancelar</button>
                    <button class="delete orange-button" @click="deleteTodo(todo.id)">Apagar</button>
                    <button class="favorite orange-button" @click="addToFavorites(todo.id)">Adicionar aos favoritos</button>
                </div>
                <div class="todo-description">
                    <div class="description todo-description" v-html="formattedDescription(todo.description)"></div>
                    <textarea v-model="editingTodo.description" placeholder="Nova descrição" class="description-change margin-block" style="white-space: pre-line; display: none" required ></textarea>
                </div>
            </li>
        </li>
    </ul>
    <div class="favorites-main">
        <h2 class="titles">Favoritos</h2>
        <div class="favorite-body">
            <div class="favorite-item" :id="'fav-'+todo.id" v-for="(todo, index) in favorites" :key="index" :style="getFavoriteItemStyle(index)">
                <img src="../assets/pin.png" style="position: absolute;width: 20%;top: -28px;left: 86%;">
                <h1 class="main-title">{{ fixTitleLength(todo.title, 15) }}</h1>
                <input v-model="editingTodo.title" placeholder="Novo título" value="${todo.title}" class="title-change big-title margin-block" required style="display: none;"/>
                <button class="edit yellow-button" @click="editTodo(todo.id, true)">Editar</button>
                <button class="confirm yellow-button" @click="confirmEdit(todo.id, true)" style="display: none;">Confirmar</button>
                <button class="cancel yellow-button" @click="cancelEdit(todo.id, true)" style="display: none;">Cancelar</button>
                <button class="delete yellow-button" @click="deleteTodo(todo.id, true)">Apagar</button>
                <button class="favorite yellow-button" @click="removeFromFavorites(todo.id, true)">Remover dos favoritos</button>
                <div class="favorite-description">
                    <div class="description" v-html="formattedDescription(todo.description)"></div>
                    <textarea v-model="editingTodo.description" placeholder="Nova descrição" class="description-change margin-block" style="white-space: pre-line; display: none" required ></textarea>
                </div>
                
            </div>
        </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
        return {
            filterTitle: "",
            filterDescription: "",
            newTodo: { id: 0, title: '', description: '' },
            numberOfFacts: 0,
            editingTodo: {id: 0, title: '', description: ''}
      }
    },
    computed: {
        todos() {
            return this.$store.state.todos
        },
        favorites() {
            return this.$store.getters.favorites
        },
        formattedDescription() {
                return (description) => description.replace(/\n/g, "<br>");
            },
        filteredTodos() {
                return this.$store.state.todos.filter(
        todo => todo.title.toLowerCase().includes(this.filterTitle.toLowerCase()) &&
        todo.description.toLowerCase().includes(this.filterDescription.toLowerCase())
        );
        }
    },
    methods: {
        addTodo() {
            if (this.newTodo.title.trim() === "" || this.newTodo.description.trim() === "") {
                alert("Por favor, introduza um titulo e uma descrição.");
                return;
            }
            
            this.$store.commit('addTodo', { ...this.newTodo, favorite: false })
            const id = this.$store.state.todos.length
            this.newTodo = { id: id, title: '', description: '' }
        },
        editTodo(id, favorite=false) {
            let prefix;
            if (favorite) prefix = "fav-"
            else prefix = "todo-"
            const todoTitle = document.getElementById(prefix+id).getElementsByTagName("h1")[0];
            const todoDescription = document.getElementById(prefix+id).getElementsByClassName('description')[0];
            const editButton = document.getElementById(prefix+id).getElementsByClassName('edit')[0];
            const favoriteButton = document.getElementById(prefix+id).getElementsByClassName('favorite')[0];
            
            const titles = document.getElementsByClassName("main-title");
            const descriptions = document.getElementsByClassName("description");
            const edits = document.getElementsByClassName("edit");
            const deletes = document.getElementsByClassName("delete");
            const favorites = document.getElementsByClassName("favorite");
            const allElemsToShow = [...titles, ...descriptions, ...edits, ...deletes, ...favorites]

            const confirmButton = document.getElementById(prefix+id).getElementsByClassName('confirm')[0];
            const cancelButton = document.getElementById(prefix+id).getElementsByClassName('cancel')[0];
            const deleteButton = document.getElementById(prefix+id).getElementsByClassName('delete')[0];
            const titleInput = document.getElementById(prefix+id).getElementsByClassName('title-change')[0];
            const descriptionInput = document.getElementById(prefix+id).getElementsByClassName('description-change')[0];

            const confirms = document.getElementsByClassName("confirm");
            const cancels = document.getElementsByClassName("cancel");
            const titleInputs = document.getElementsByClassName("title-change");
            const descriptionInputs = document.getElementsByClassName("description-change");
            const todo = this.$store.state.todos.find(todo => todo.id === id);
            const allElemsToHide = [...confirms,...cancels, ...titleInputs, ...descriptionInputs];

            for (let elem of allElemsToHide) {
                elem.style.display = "none";
            }

            for (let elem of allElemsToShow) {
                elem.removeAttribute("style");
            }
            
            todoTitle.style.display = "none";
            todoDescription.style.display = "none";
            editButton.style.display = "none";
            deleteButton.style.display = "none";
            favoriteButton.style.display = "none";
            deleteButton.style.display = "none";
            favoriteButton.style.display = "none";
            titleInput.value = todo.title;
            descriptionInput.value = todo.description;
            this.editingTodo.title = todo.title;
            this.editingTodo.description = todo.description;


            confirmButton.removeAttribute("style");
            cancelButton.removeAttribute("style");
            titleInput.removeAttribute("style");
            descriptionInput.removeAttribute("style");

        },
        confirmEdit(id, favorite=false) {
            if (this.editingTodo.title.trim() === "" || this.editingTodo.description.trim() === "") {
                alert("Por favor, introduza um titulo e uma descrição.");
                return;
            }

            let prefix;
            if (favorite) prefix = "fav-"
            else prefix = "todo-"

            const todo = this.$store.state.todos.find(todo => todo.id === id)
            const index = this.$store.state.todos.findIndex(todo => todo.id === id)
            this.$store.commit('editTodo', {
                            index: index,
                            title: this.editingTodo.title,
                            description: this.editingTodo.description,
                            favorite: todo.favorite,
                            id: todo.id
                        })

            this.editingTodo = {id: 0, title: '', description: ''}
            
            const todoTitle = document.getElementById(prefix+id).getElementsByTagName("h1")[0];
            const todoDescription = document.getElementById(prefix+id).getElementsByClassName('description')[0];
            const editButton = document.getElementById(prefix+id).getElementsByClassName('edit')[0];
            const deleteButton = document.getElementById(prefix+id).getElementsByClassName('delete')[0];
            const favoriteButton = document.getElementById(prefix+id).getElementsByClassName('favorite')[0];
            const confirmButton = document.getElementById(prefix+id).getElementsByClassName('confirm')[0];
            const cancelButton = document.getElementById(prefix+id).getElementsByClassName('cancel')[0];
            const titleInput = document.getElementById(prefix+id).getElementsByClassName('title-change')[0];
            const descriptionInput = document.getElementById(prefix+id).getElementsByClassName('description-change')[0];

            todoTitle.innerText = this.fixTitleLength(todo.title, 40)
            todoDescription.innerText = this.formattedDescription(todo.description);
            editButton.removeAttribute("style");
            deleteButton.removeAttribute("style");
            favoriteButton.removeAttribute("style");
            todoTitle.removeAttribute("style");
            todoDescription.removeAttribute("style");
            confirmButton.style.display = "none";
            cancelButton.style.display = "none";
            titleInput.style.display = "none";
            descriptionInput.style.display = "none";
            
        },
        cancelEdit(id, favorite=false) {
            let prefix;
            if (favorite) prefix = "fav-"
            else prefix = "todo-"
            const todo = this.$store.state.todos.find(todo => todo.id === id);
            const todoTitle = document.getElementById(prefix+id).getElementsByTagName("h1")[0];
            const todoDescription = document.getElementById(prefix+id).getElementsByClassName('description')[0];
            const editButton = document.getElementById(prefix+id).getElementsByClassName('edit')[0];
            const deleteButton = document.getElementById(prefix+id).getElementsByClassName('delete')[0];
            const favoriteButton = document.getElementById(prefix+id).getElementsByClassName('favorite')[0];
            const confirmButton = document.getElementById(prefix+id).getElementsByClassName('confirm')[0];
            const cancelButton = document.getElementById(prefix+id).getElementsByClassName('cancel')[0];
            const titleInput = document.getElementById(prefix+id).getElementsByClassName('title-change')[0];
            const descriptionInput = document.getElementById(prefix+id).getElementsByClassName('description-change')[0];

            todoTitle.innerText = this.fixTitleLength(todo.title, 40)
            todoDescription.innerText = this.formattedDescription(todo.description);
            editButton.removeAttribute("style");
            deleteButton.removeAttribute("style");
            favoriteButton.removeAttribute("style");
            todoTitle.removeAttribute("style");
            todoDescription.removeAttribute("style");
            confirmButton.style.display = "none";
            cancelButton.style.display = "none";
            titleInput.style.display = "none";
            descriptionInput.style.display = "none";
        },
        deleteTodo(id) {
            const index = this.$store.state.todos.findIndex(todo => todo.id === id)
            this.$store.commit('deleteTodo', index)
        },
        addToFavorites(id) {
            const index = this.$store.state.todos.findIndex(todo => todo.id === id)
            this.$store.commit('addToFavorites', index)
        },
        removeFromFavorites(id) {
            const index = this.$store.state.todos.findIndex(todo => todo.id === id)
            this.$store.commit('removeFromFavorites', index)
        },
        getTop(index) {
            return String(Math.floor(index/2) * 340 + 20) + "px";
        },
        getLeft(index) {
            return String(index % 2 * 360 + 40) + "px";
        },
        getFavoriteItemStyle(index) {
            return {
                top: this.getTop(index),
                left: this.getLeft(index)
            }
        },
        createFacts() {
            if (this.numberOfFacts > 1)
                fetch(`https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount=${this.numberOfFacts}`)
                    .then(response => response.json())
                    .then(data => {
                        for (let fact of data) {
                            this.newTodo.title = "Cat fact!";
                            this.newTodo.description = fact["text"];
                            this.addTodo();
                        } })
            else fetch(`https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount=${this.numberOfFacts}`)
                    .then(response => response.json())
                    .then(data => {
                            this.newTodo.title = "Cat fact!";
                            this.newTodo.description = data["text"];
                            this.addTodo();
                         })

        },
        fixTitleLength(text,n) {
            if (text.length > n) return text.slice(0, n) + "(...)"
            return text
        },
        getHeight(){
        return {height: + window.innerHeight + "px"}
        }     
    }
  }
  </script>