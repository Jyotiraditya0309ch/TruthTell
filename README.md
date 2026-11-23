# TruthTell

The React frontend is in `frontend`. Install its dependencies with `npm ci` and start Vite with `npm run dev`.

The Django backend is in `Primary Backend/Fake_News_Detection_Backend/backend`. Copy `Primary Backend/.env.example` to `Primary Backend/.env` and set a Django secret key. The JWT signing key defaults to the Django secret key. Set `MONGODB_URI` if you use a remote MongoDB instance. Analysis features also use service credentials from the environment.

The repository omits the large GloVe embeddings, LSTM weights, and both deepfake checkpoints. Model-backed analysis requires restoring those files to their original local paths.
