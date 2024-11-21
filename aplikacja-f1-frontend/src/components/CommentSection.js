import React, { useEffect, useState } from 'react';
import api from '../services/api';

const CommentSection = ({ raceId }) => {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');

  useEffect(() => {
    const fetchComments = async () => {
      try {
        const response = await api.get(`comments/?race=${raceId}`);
        setComments(response.data);
      } catch (error) {
        console.error('Error fetching comments', error);
      }
    };

    fetchComments();
  }, [raceId]);

  const handleAddComment = async () => {
    try {
      const response = await api.post('comments/', {
        race: raceId,
        content: newComment,
      });
      setComments([...comments, response.data]);
      setNewComment('');
    } catch (error) {
      console.error('Error adding comment', error);
    }
  };

  const handleDeleteComment = async (commentId, userId) => {
    const currentUserId = localStorage.getItem('user_id');
    const isAdmin = localStorage.getItem('is_admin') === 'true';
  
    if (isAdmin || currentUserId === userId) {
      try {
        await api.delete(`comments/${commentId}/`);
        setComments(comments.filter((comment) => comment.id !== commentId));
      } catch (error) {
        console.error('Error deleting comment', error);
      }
    } else {
      alert('Nie masz uprawnień do usunięcia tego komentarza');
    }
  };
  

  return (
    <div>
      <h3>Comments</h3>
      <ul>
        {comments.map((comment) => (
          <li key={comment.id}>
            {comment.content} - {comment.user.username}
            <button onClick={() => handleDeleteComment(comment.id)}>Delete</button>
          </li>
        ))}
      </ul>
      <textarea
        value={newComment}
        onChange={(e) => setNewComment(e.target.value)}
      />
      <button onClick={handleAddComment}>Add Comment</button>
    </div>
  );
};

export default CommentSection;
