import { initializeApp } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-app.js";
import { getAuth, signInWithPopup, GoogleAuthProvider, signOut } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-auth.js";

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyB3Dya2tTYef2VlaxZVQVxkO_Avfc5UOfg",
  authDomain: "mindbot-9bcc7.firebaseapp.com",
  projectId: "mindbot-9bcc7",
  storageBucket: "mindbot-9bcc7.appspot.com",
  messagingSenderId: "80842807023",
  appId: "1:80842807023:web:68f43ebf6e5875d21f6d1a"
};

document.addEventListener('DOMContentLoaded', () => {
  // Initialize Firebase
  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app);
  auth.languageCode = 'en';

  // Google Auth Provider
  const provider = new GoogleAuthProvider();

  // Google Login
  const googleLogin = document.getElementById("google-login-button");
  if (googleLogin) {
    googleLogin.addEventListener("click", function() {
      signInWithPopup(auth, provider)
        .then((result) => {
          window.location.href = '/Main/index.html'; // Redirect on successful login
        }).catch((error) => {
          console.error("Error signing in with Google:", error.code, error.message);
        });
    });
  } else {
    console.error("Google login button not found");
  }

  // Logout functionality
  const logoutButton = document.getElementById("google-logout-button");
  if (logoutButton) {
    logoutButton.addEventListener("click", function() {
      signOut(auth).then(() => {
        console.log('User signed out.');
        window.location.href = 'login.html'; // Redirect on logout
      }).catch((error) => {
        console.error("Error signing out:", error);
      });
    });
  } else {
    console.error("Logout button not found");
  }
});
