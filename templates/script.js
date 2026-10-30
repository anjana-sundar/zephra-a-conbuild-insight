// Import Firebase modules (modular v10+)
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.3/firebase-app.js";
import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut } from "https://www.gstatic.com/firebasejs/10.12.3/firebase-auth.js";

// ✅ Your Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyB-XIg1fnBAR1LgzI7SYaoSO_uRYxi-6dc",
  authDomain: "website-84dc4.firebaseapp.com",
  projectId: "website-84dc4",
  storageBucket: "website-84dc4.firebasestorage.app",
  messagingSenderId: "977323588732",
  appId: "1:977323588732:web:424ec7ca1a859970175df9",
  measurementId: "G-8EQYQS3TKK"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Tab switching
const loginTab = document.getElementById("login-tab");
const signupTab = document.getElementById("signup-tab");
const loginForm = document.getElementById("login-form");
const signupForm = document.getElementById("signup-form");

loginTab.addEventListener("click", () => {
  loginForm.classList.add("active");
  signupForm.classList.remove("active");
  loginTab.classList.add("active");
  signupTab.classList.remove("active");
});

signupTab.addEventListener("click", () => {
  signupForm.classList.add("active");
  loginForm.classList.remove("active");
  signupTab.classList.add("active");
  loginTab.classList.remove("active");
});

// Login
loginForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const email = document.getElementById("login-email").value;
  const password = document.getElementById("login-password").value;

  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      alert("✅ Logged in as " + userCredential.user.email);
      window.location.href = "home.html"; // redirect after login
    })
    .catch((error) => {
      alert("❌ " + error.message);
    });
});

// Signup
signupForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const email = document.getElementById("signup-email").value;
  const password = document.getElementById("signup-password").value;

  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      alert("✅ Account created for " + userCredential.user.email);
    })
    .catch((error) => {
      alert("❌ " + error.message);
    });
});

// Logout
document.getElementById("logout-btn").addEventListener("click", () => {
  signOut(auth)
    .then(() => {
      alert("🚪 Logged out");
      window.location.href = "login.html"; // redirect back to login
    })
    .catch((error) => alert("❌ " + error.message));
});
