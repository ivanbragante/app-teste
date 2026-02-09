import React from 'react';

const PostCard = ({ post }) => {
  return (
    <div className="card">
      <div>
        <h3 className="card-title">{post.title}</h3>
        <div className="meta">
            <div className="metric">
                <span>🔥</span>
                <span>{post.engagement}</span>
            </div>
          <div className="metric">
            <span>⬆️</span>
            <span>{post.ups}</span>
          </div>
          <div className="metric">
            <span>💬</span>
            <span>{post.num_comments}</span>
          </div>
        </div>
      </div>
      <a href={post.permalink} target="_blank" rel="noopener noreferrer" className="btn-read">
        Read Post
      </a>
    </div>
  );
};

export default PostCard;
