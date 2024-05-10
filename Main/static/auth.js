document.getElementById('login-button').addEventListener('click', (event) => {
  event.preventDefault(); 

  const email = document.getElementById('loginId').value;
  const password = document.getElementById('password').value;

  fetch('/login', { 
    method: 'POST',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email: email, password: password, action: 'login' })
  })
  .then(response => {
    // Handle response if needed
  })
  .catch(error => {
    console.error('Error:', error);
  });
});

// document.getElementById('signup-button').addEventListener('click', (event) => {
//   event.preventDefault();

//   const email = document.getElementById('loginId').value;
//   const password = document.getElementById('password').value;

//   fetch('/login', { 
//     method: 'POST',
//     headers: {
//       'Accept': 'application/json',
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({ email: email, password: password, action: 'signup' })
//   })
//   .then(response => {
//     // Handle response if needed
//   })
//   .catch(error => {
//     console.error('Error:', error);
//   });
// });
