const express = require('express');
const bodyParser = require('body-parser');
const { OpenAI } = require('openai');
require('dotenv').config();

const app = express();
app.use(bodyParser.json());

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

app.post("/chat", async (req, res) => {
  const chat = req.body.chat;

  if (!chat) {
    return res.status(400).send("Missing 'chat' in request body");
  }

  try {
    const response = await openai.chat.completions.create({
      model: "gpt-3.5-turbo", // ✅ Use a model you have access to
      messages: [
        {
          role: "user",
          content: chat,
        },
      ],
    });

    res.send(response.choices[0].message.content);
  } catch (error) {
    console.error("Error from OpenAI:", error);

    if (error.status === 429) {
      res.status(429).send("Rate limit exceeded. Check your OpenAI quota and billing.");
    } else if (error.status === 404) {
      res.status(404).send("Requested model not found. Check your model name or access.");
    } else {
      res.status(500).send("Internal server error.");
    }
  }
});

app.listen(3000, () => {
  console.log("Server is running on port 3000");
});
