# Schema + Endpoints

## Endpoints

| Category | Endpoint | Method | Role | Description |
| --- | --- | --- | --- | --- |
| **Authentication** | `/auth/register` | POST | Any | Registers a new user with a role (Admin, Buyer, Seller). |
|  | `/auth/login` | POST | Any | Authenticates a user and returns an access token. |
| **Products** | `/preload-products/` | POST | Any | Preloads product data from DummyJSON into the database. |
|  | `/products/` | POST | Seller | Allows Sellers to add new products. |
|  | `/products/` | GET | Any | Fetches a list of all available products. |
|  | `/products/{product_id}` | GET | Any | Retrieves details of a specific product. |
|  | `/products/{product_id}` | PUT | Seller | Updates product details (only by the Seller who uploaded it). |
|  | `/products/{product_id}` | DELETE | Seller | Deletes a product (only by the Seller who uploaded it). |
|  | `/products/upload-pdf`

** | POST | Seller | Allows Sellers to upload a PDF containing product details. |
|  | `/products/download/{product_id}` | GET | Any | Enables users to download product details as a file. |
| **Cart & Orders** | `/cart/add` | POST | Buyer | Adds a product to the Buyer's cart. |
|  | `/cart/remove/{product_id}` | DELETE | Buyer | Removes a product from the Buyer's cart. |
|  | `/cart/` | GET | Buyer | Fetches the Buyer's current cart contents. |
|  | `/orders/` | POST | Buyer | Places an order for items in the Buyer's cart. |
|  | `/orders/` | GET | Buyer | Retrieves a list of the Buyer's past orders. |
|  | `/orders/{order_id}` | GET | Buyer | Fetches details of a specific order. |
| **Complaints** | `/complaints/` | POST | Buyer | Allows Buyers to file a complaint, possibly with images. |
|  | `/complaints/` | GET | Seller | Retrieves all complaints for Admin review. |
|  | `/complaints/{complaint_id}` | GET | Seller | Fetches details of a specific complaint. |
| **File Uploads** | `/upload/product-image` ❌ | POST | Seller | Uploads an image for a product and stores it in Google Cloud Storage. |
|  | `/upload/complaint-file` | POST | Buyer | Uploads a file related to a complaint. |
| **Users & RBAC** | `/users/me` | GET | Any | Fetches details of the currently authenticated user. |
|  | `/users/` | GET | Admin | Retrieves a list of all users. |
|  | `/users/{user_id}/role` | PUT | Admin | Updates the role of a specific user. |

<aside>
⚠️

Admin should be able to access all the routes. 🙏🏻

</aside>

## Database Schema (MongoDB)

---

### **User Schema (Authentication & Role Management)**

```python
class User(Model):
    name: str
    email: EmailStr
    password_hash: str  
    role: Literal["admin", "buyer", "seller"]  
```

---

### **Product Schema (Based on DummyJSON)**

```python
class Product(Model):
    title: str
    description: str
    category: str
    price: float
    rating: float
    brand: str
    images: List[str]
    seller_id: ObjectId
    quantity: int
```

---

### **Cart Schema (Buyer’s Shopping Cart)**

```python
class CartItem(Model):
    user_id: ObjectId -> foregin key
    product_id: ObjectId -> foregin key
    quantity: int
```

---

### **Order Schema (Buyers' Orders)**

```python
class OrderItem(Model): # ---> structure
    quantity: int
    price: float

class Order(Model): # ---> Schema
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: Literal["pending", "shipped", "delivered", "cancelled"]
```

---

### **Complaint Schema (Buyer Complaints)**

```python
class Complaint(Model):
    user_id: ObjectId
    order_id: ObjectId
    product_id: ObjectId
    issue: str
    image_url: str
    status: Literal["open", "rejected"]
```

---

### **File Upload Schema (Google Cloud Storage)**

```python
class FileUpload(Model):
    user_id: ObjectId
    file_url: str
    file_type: Literal["product", "complaint"]
```

<aside>
🚧

Add createdAt, updatedAt or timestamps for all the collections!

</aside>
