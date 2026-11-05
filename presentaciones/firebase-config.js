// Configuración web de Firebase para el proyecto artificialartificer.
// Estos valores identifican al proyecto; no son secretos. La protección está en firestore.rules.
// Obténlos con: firebase apps:sdkconfig WEB <APP_ID> --project artificialartificer
export const firebaseConfig = {
  apiKey: "AIzaSyA-LocoJdbkiaQ-pFzfEpqECq5vyQWceTY",
  authDomain: "artificialartificer.firebaseapp.com",
  projectId: "artificialartificer",
  storageBucket: "artificialartificer.firebasestorage.app",
  messagingSenderId: "653870572763",
  appId: "1:653870572763:web:6be38e76a918aa7d6918fe"
};

// Formato de matrícula aceptado (se convierte a mayúsculas). Debe coincidir con firestore.rules.
export const MATRICULA = /^[A-Z0-9]{4,12}$/;