import { useState } from "react";
import "./App.css";

interface SubredditItem {
  subreddit: string;
  keywords: string[];
}

interface RequestData {
  items: SubredditItem[];
  limit: number;
}

interface SubredditResult {
  subreddit: string;
  posts: ResponseItem[];
}

interface ResponseData {
  items: SubredditResult[];
}

interface ResponseItem {
  title: string;
  has_image: boolean;
}

function App() {

  const [subreddit, setSubreddit] = useState("");
  const [keywords, setKeywords] = useState("");
  const [limit, setLimit] = useState(5);

  const [result, setResult] = useState<ResponseData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.SubmitEvent) => {
    e.preventDefault();

    if (subreddit.length === 0) {
      setError("Please provide subreddit's name")
      return
    }

    setError(null);
    setLoading(true);

    const subreddits = subreddit.split(",").map(s => s.trim());

    const items: SubredditItem[] = subreddits.map(sub => ({
      subreddit: sub,
      keywords: keywords.split(",").map(k => k.trim())
    }));

    const body: RequestData = { items, limit };

    try {

      const res = await fetch("http://localhost:8000/parse", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
      });

      const data = await res.json();
      setResult(data);
     
    } 
    
    catch (err: any) {
      console.error(err);
      setError(err.message || "Unknown error");
    } 
    
    finally {
      setLoading(false);
    }
  };

  const renderResult = () => {
    return result!.items.map((item) => (
            <div key={item.subreddit} style={{ marginBottom: "16px" }}>
              <h3>/r/{item.subreddit}</h3>

                {item.posts.length === 0 ? (
                  <p>No posts found</p>
                ) : (
                  <ul>
                    {item.posts.map((post, i) => (
                      <li key={i}>
                          {post.title}
                          <span
                            style={{
                              marginLeft: "8px",
                              padding: "2px 6px",
                              borderRadius: "6px",
                              fontSize: "12px",
                              background: post.has_image ? "#4caf50" : "#ccc",
                              color: "white"
                            }}
                          >
                            {post.has_image ? "Image included" : "No image"}
                          </span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ))
  }

  return (
    <div style={{ padding: "16px" }}>
      <h1 style={{color: "white"}}>Reddit Parser</h1>
      <form className="form" onSubmit={handleSubmit}>
        <div className="form__item">
          <label>Subreddit: </label>
          <input
            value={subreddit}
            onChange={e => setSubreddit(e.target.value)}
          />
        </div>
        <div className="form__item ">
          <label>Keywords (comma separated, optional): </label>
          <input
            value={keywords}
            onChange={e => setKeywords(e.target.value)}
          />
        </div>
        <div className="form__item">
          <label>Limit: </label>
          <input
            type="number"
            value={limit}
            onChange={e => setLimit(Number(e.target.value))}
          />
        </div>
        <button type="submit" disabled={loading} style={{width: "175px"}}>
          {loading ? "Loading..." : "Parse"}
        </button>
      </form>

      {error && 
      <div style={{ color: "red", marginTop: "12px" }}>Error: {error}</div>}

     {result && (
        <div className="result-container">
        <h2>Result:</h2>
        {renderResult()}
      </div>
)}

</div>
  );
}

export default App;