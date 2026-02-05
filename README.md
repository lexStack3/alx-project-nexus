# [FastYums – E-Commerce Backend Capstone Project](https://docs.google.com/document/d/1pi-CmkaLidQ-opmqMgSXov6bgMxKdVPXkILOS_m_0Xw/edit?usp=sharing)
(ProDev Backend Engineering | Project Nexus)

FastYums is a role-based, multi-vendor **E-Commerce backend system** developed as part of **Project Nexus**, the graduation capstone for the **ProDev Backend Engineering Program**.  
The project demonstrates the design and implementation of a real-world backend application using **Django** and **Django REST Framework**, with strong emphasis on scalability, security, database efficiency, and REST API best practices.

---

## Project Objectives
This project was built to fulfill the core objectives of Project Nexus:
- Apply backend engineering skills to a real-world e-commerce problem
- Design and implement scalable RESTful APIs
- Demonstrate strong database modeling and optimization
- Implement secure authentication and role-based authorization
- Deliver clear documentation and a deployable backend system

---

## Core E-Commerce Features

### 1. Authentication & Authorization
- JWT-based authentication using **SimpleJWT**
- Role-based access control:
  - `CUSTOMER`
  - `VENDOR`
  - `COURIER`
  - `ADMIN`
- Custom permission classes enforcing role and resource ownership

### 2. Product & Category Management
- Full CRUD APIs for products and categories
- Vendors can only manage their own products
- Product availability and stock control

### 3. Product Discovery
- Search by product name and description
- Filter by category
- Sort by price (ascending / descending)
- Paginated API responses for large datasets

### 4. Order Management (Transactional Flow)
- Server-side order creation with atomic price calculation
- Order lifecycle:
  - `PLACED` → `ACCEPTED` → `READY_FOR_PICKUP` → `ASSIGNED` → `OUT_FOR_DELIVERY` → `DELIVERED` / `CANCELLED`
- Transaction-safe operations to ensure consistency

### 5. Delivery & Fulfillment
- Courier registration and availability tracking
- Delivery assignment workflow
- Race-condition prevention during courier acceptance
- Courier-managed delivery status updates

### 6. Notification System
- Database-backed in-app notifications
- Notifications triggered by order and delivery state changes
- REST endpoints for retrieval and read-status updates

---

## Database Design & ERD
- Relational schema designed using **MySQL**
- Proper normalization and foreign key constraints
- Indexed fields for performance optimization:
- Product (category, availability)
- Order (status)
- DeliveryAssignment (status)
- [Entity Relationship Diagram](https://docs.google.com/document/d/1OZl5Solm--XdR3f9Q3SF3EhSFMMvnavmz2Astp82rrI/edit?usp=drive_link) (ERD) designed and shared separately for mentor review

---

## API Surface (Sample Endpoints)

**Authentication**
- `POST /api/v1/auth/register/`
- `POST /api/v1/auth/login/`

**Products**
- `GET /api/v1/products/`
- `POST /api/v1/products/`
- `GET /api/v1/products/{id}/`
- `PUT /api/v1/products/{id}/`
- `DELETE /api/v1/products/{id}/`

**Orders**
- `POST /api/v1/orders/`
- `GET /api/v1/orders/{id}/`
- `PATCH /api/v1/orders/{id}/`

**Delivery**
- `POST /api/v1/orders/{id}/assign-delivery/`
- `POST /api/v1/delivery/{assignment_id}/accept/`

---

## Security Considerations
- JWT authentication with refresh tokens
- Custom role-based permission classes
- Ownership checks for all protected resources
- Minimal exposure of courier-sensitive data
- Environment-based configuration for secrets

---

## Testing Strategy
- Unit tests for models, serializers, and permissions
- API tests for authentication, product CRUD, and order flows
- Integration tests covering end-to-end scenarios
- Edge case handling (unauthorized access, unavailable items)

---

## Deployment
- Deployed on **PythonAnywhere**
- Production setup includes:
- Gunicorn WSGI server
- Static file handling
- Environment-based settings
- Live backend supports full order and delivery workflows

---

## Repository Structure
- `accounts/` – users, authentication, roles
- `vendors/` – vendor profiles
- `products/` – products and categories
- `orders/` – orders and order items
- `delivery/` – courier and delivery assignments
- `notifications/` – in-app notifications

---

## Future Improvements
- Background tasks with Celery & RabbitMQ
- Payment gateway integration (Paystack / Stripe)
- Real-time notifications using WebSockets
- Dockerized deployment
- CI/CD pipelines with GitHub Actions

---

## Project Nexus Compliance
✔ RESTful E-Commerce APIs  
✔ JWT authentication & RBAC  
✔ Filtering, sorting, pagination  
✔ Optimized relational database  
✔ API documentation  
✔ Deployed backend application  

---

## Author
**Alexander Edim**  
ProDev Backend Engineering Learner  
Project Nexus – Graduation Capstone