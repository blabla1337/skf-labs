function App() {
  const [value, setValue] = React.useState("");
  const [message, setMessage] = React.useState(false);
  const handleChange = (e) => setValue(e.target.value);
  const clear = () => setValue("");
  const styles = {
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
    alignItems: "start",
  };
  return (
    <div style={styles}>
      <input
        type="password"
        value={value}
        onChange={handleChange}
        className="input-auth"
      />
      {message && <p>Incorrect credentials</p>}
      <button
        onClick={() => {
          clear();
          setMessage(true);
        }}
        className="auth-btn"
      >
        Confirm
      </button>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("r-app")).render(<App />);
