import { initializeApp } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-app.js";
import { getFirestore, doc, setDoc } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-firestore.js";
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
  const db = getFirestore(app);
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
          const user = result.user;
          const userRef = doc(db, "users", user.uid);
          setDoc(userRef, {
            displayName: user.displayName,
            email: user.email,
            lastLogin: new Date()
          }, { merge: true })
          .then(() => {
            console.log("User data saved to Firestore.");
            // Redirect to index.html after successful login
            window.location.href = '../templates/index.html';
          }).catch((error) => {
            console.error("Error signing in with Google:", error.code, error.message);
          });
        })
        .catch((error) => {
          console.error("Error signing in with Google:", error.code, error.message);
        });
    });
  } else {
    console.error("Google login button not found");
  }
})