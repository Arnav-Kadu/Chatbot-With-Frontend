import { initializeApp } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-app.js";
import { getFirestore, doc, setDoc,getDoc } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-firestore.js";
import { getAuth, signInWithPopup, GoogleAuthProvider, signOut,signInWithRedirect,signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-auth.js";

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyB3Dya2tTYef2VlaxZVQVxkO_Avfc5UOfg",
  authDomain: "mindbot-9bcc7.firebaseapp.com",
  projectId: "mindbot-9bcc7",
  storageBucket: "mindbot-9bcc7.appspot.com",
  messagingSenderId: "80842807023",
  appId: "1:80842807023:web:68f43ebf6e5875d21f6d1a"
};
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);
auth.languageCode = 'en'; 

// Google Auth Provider
const provider = new GoogleAuthProvider();

// **Login Function**
const loginWithEmailAndPassword = async (email, password) => {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    window.location.href="/";
    console.log("Login successful with email/password");
  } catch (error) {
    console.error("Login error:", error.code, error.message);
  }
};

// **Event Listeners**
document.getElementById('login-button').addEventListener('click', () => {
  const email = document.getElementById('loginId').value;
  const password = document.getElementById('password').value;
  loginWithEmailAndPassword(email, password);
});

document.getElementById('signup-button').addEventListener('click', () => {
  const email = document.getElementById('loginId').value;
  const password = document.getElementById('password').value;
  signupWithEmailAndPassword(email, password);
});

document.getElementById('google-login-button').addEventListener('click', () => {
  loginWithGooglePopup();
});