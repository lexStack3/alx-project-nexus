# E-Commerce Backend Capstone Project <br> (ProDev Backend Engineering)
FastYums is a role-based, multi-vendor **E-Commerce backend system** built as part of **Project Nexus**, the capstone project for the **ProDev Backend Engineering Program**. The project demonstrates the design and implementation of a real-world backend application using Django and Django REST Framework, with a strong focus on scalability, security, database efficiency, and API best practices.
[Read More...](https://docs.google.com/document/d/1pi-CmkaLidQ-opmqMgSXov6bgMxKdVPXkILOS_m_0Xw/edit?usp=sharing)
## Project Objectives
This project was built to satisfy the core objectives of Project Nexus:
- Apply backend technologies to real-world e-commerce problem
- Design and implement scalable RESTful APIs
- Demonstrate strong database modeling and optimization skills
- Implement secure authentication and role-based authorization
- Produce clear documentation and a deployable backend system

## E-Commerce Features Implemented
#### 1. User Authentication and Authorization
- JWT-based authentication using **SimpleJWT**
- Role-based access control:
  - `CUSTOMER`
  - `VENDOR`
  - `COURIER`
  - `ADMIN`
- Secure access to resources based on ownership and role
#### 2. Product and Category Management (CRUD)
- Full CRUD APIs for product (meals)
- Category management for organizing products
- Vendors can only manage their own products
- Product availability control (in stock / out of stock)
#### 3. Product Discovery
- Search products by name and description
- Filter products by category
- Sort products by price (ascending / descending)
- Paginated API response for large datasets
#### 4. Order Management (Transactional E-Commerce Flow)
- Server-side order creation with price calculation
- Order lifecycle management:
  - `PLACED` → `ACCEPTED` → `READY_FOR_PICKUP` → `ASSIGNED` → `OUT_FOR_DELIVERY` → `DELIVERED` / `CANCELLED`
- Atomic order creation to ensure data consistency
#### 5. Delivery & Fulfillment
- Courier registration and availability tracking
- Delivery assignment workflow
- Transaction-safe courier acceptance to prevent race conditions
- Delivery status updates managed by assigned courier
#### 6. Notifications System
- In-app notification system backed by the database
- Notifications triggered by order and delivery status changes
- Users can retrieve and mark notifications as read via REST APIs

## Database Design and Optimization
- Relational database schema designed using **MySQL**
- Proper normalization and use of foreign keys
- Indexed fields for performance optimization:
  - Product (category, availability)
  - Order (status)
  - DeliveryAssignment (status)
- Efficient querying with Django ORM

## Security Considerations
- JWT authentication with access and refresh tokens
- Custom permission classes enforcing role-based access
- Resource ownership validation (users access only their data)
- Minimal exposure of sensitive courier information
- Environment-based configuration for secrets

## Testing Strategy
- Unit tests for models, serializers, and permission classes
- API tests for authentication, product CRUD, and order flows
- Integration tests covering end-to-end e-commerce scenarios
- Edge case handling (unauthorized access, unavailable product)

## API Documentation
- Interactive API documentation using **Swagger/OpenAPI**
- Postman collection available for API testing and demonstration
- All endpoints follow RESTful conventions and HTTP standards

## Deployment
- Deploy on **PythonAnywhere**
- Production configuration include:
  - Gunicorn WSGI server
  - Static file handling
  - Environment-based settings
- Live API supports full order placement and delivery workflow

## Repository Structure (High-Level)
- `accounts/` - authentication, user, roles
- `vendors/` - vendor onboarding and profiles
- `products/` - products and categories
- `orders/` - order and order item management
- `delivery/` - courier and delivery assignments
- `notifications/` - in-app notification system

## Future Improvements (Post-Capstone)
- Background tasks with Celery and RabbitMQ
- Real payment gateway integration (Paystack / Stripe)
- Real-time notifications using WebSockets
- Dockerized deployment
- CI/CD pipelines using GitHub Actions

## Project Nexus Compliance Summary
✔ RESTful E-Commerce APIs implemented<br>
✔ JWT authentication and authorization<br>
✔ Filtering, sorting, and pagination supported<br>
✔ Optimized relational database schema<br>
✔ API documentation provided<br>
✔ Deployed backend application

## Author
**Alexander Edim**
<br>ProDev Backend Engiheering Learner
<br>Project Nexus - Graduation Capstone