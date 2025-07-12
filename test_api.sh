#!/bin/bash

BASE_URL="http://localhost:70"
USER_EMAIL="testuser@example.com"
USER_FIRST="Test"
USER_LAST="User"

echo "🔄 Health check..."
curl -s -w "\n➡️ HTTP Status: %{http_code}\n" "$BASE_URL/health"
echo "-----------------------------------------------------"

echo "👤 Creating user..."
USER_ID=$(curl -s -X POST "$BASE_URL/users/" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$USER_EMAIL\", \"first_name\": \"$USER_FIRST\", \"last_name\": \"$USER_LAST\"}" | jq -r '.id')

echo "✅ Created user with ID: $USER_ID"
echo "-----------------------------------------------------"

echo "👥 Fetching all users..."
curl -s "$BASE_URL/users/" | jq
echo "-----------------------------------------------------"

echo "👁️ Getting user by ID $USER_ID..."
curl -s "$BASE_URL/users/$USER_ID" | jq
echo "-----------------------------------------------------"

echo "✏️ Updating user $USER_ID..."
curl -s -X PUT "$BASE_URL/users/$USER_ID" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "UpdatedName"}' | jq
echo "-----------------------------------------------------"

echo "📝 Creating post for user $USER_ID..."
POST_ID=$(curl -s -X POST "$BASE_URL/posts/" \
  -H "Content-Type: application/json" \
  -d "{\"title\": \"My First Post\", \"content\": \"This is a test post.\", \"author_id\": $USER_ID}" | jq -r '.id')

echo "✅ Created post with ID: $POST_ID"
echo "-----------------------------------------------------"

echo "📋 Fetching all posts..."
curl -s "$BASE_URL/posts/" | jq
echo "-----------------------------------------------------"

echo "🔍 Getting post by ID $POST_ID..."
curl -s "$BASE_URL/posts/$POST_ID" | jq
echo "-----------------------------------------------------"

echo "✏️ Updating post $POST_ID..."
curl -s -X PUT "$BASE_URL/posts/$POST_ID" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Post Title", "is_published": true}' | jq
echo "-----------------------------------------------------"

echo "🗑️ Deleting post $POST_ID..."
curl -s -X DELETE "$BASE_URL/posts/$POST_ID"
echo "✅ Post deleted"
echo "-----------------------------------------------------"

echo "🗑️ Deleting user $USER_ID..."
curl -s -X DELETE "$BASE_URL/users/$USER_ID"
echo "✅ User deleted"
echo "-----------------------------------------------------"

echo "✅ All tests completed."

