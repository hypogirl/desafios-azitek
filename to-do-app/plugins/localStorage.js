export default store => {
    // Subscribe to mutations (whenever state changes)
    store.subscribe((mutation, state) => {
      // Save the entire state to local storage
      localStorage.setItem('myAppStore', JSON.stringify(state));
    });
  
    // Load state from local storage during app initialization
    const savedState = localStorage.getItem('myAppStore');
    if (savedState) {
      store.replaceState(JSON.parse(savedState));
    }
  };