require('dotenv').config(); // 👈 tout en haut
const express = require('express');
const cors = require('cors');
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY); // 👈 ça doit rester comme ça


const app = express();
app.use(cors({
  origin: "*", // Pour test local, autorise toutes origines
  methods: ["GET", "POST"],
  allowedHeaders: ["Content-Type"]
}));

// 👈 Autorise les requêtes cross-origin
app.use(express.static("public"));
app.use(express.json());

const PORT = 5051;

app.post("/create-checkout-session", async (req, res) => {
  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ["card"],
      line_items: [
        {
          price_data: {
            currency: "eur",
            product_data: { name: "Produit exemple" },
            unit_amount: 2000, 
          },
          quantity: 1,
        },
      ],
      mode: "payment",
      success_url: "http://localhost:5000/success.html",
      cancel_url: "http://localhost:5000/cancel.html",
    });

    res.json({ sessionId: session.id, publicKey: "pk_test_51O51rjArOje5RHk1efwIUykr9RbABxTf2cPREJJCXeBYDd0tXXnDcX6i37EeMA5DQzj9feOutXHEQ5Q6z1nUOoHb009DhpNlKN" });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Erreur lors de la création de la session" });
  }
});

app.listen(PORT, () => {
  console.log(`Serveur lancé sur http://localhost:${PORT}`);
});
