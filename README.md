# SMART GRID FOR LOAD BALANCING
## Overview
This project implements a smart grid simulation for industrial load balancing, designed to monitor energy consumption across multiple machines, predict short-term demand, and proactively control loads to reduce peak electricity costs while maintaining operational safety. The system models a realistic monitor–predict–control loop commonly used in industrial energy management and smart grid applications.

## System Design

Industrial machines are modeled with priority levels (critical, medium, non-critical) and maximum power ratings. A Python-based sensor simulation continuously generates power usage data, which is stored in an SQLite database to emulate edge-deployed monitoring systems. This setup enables real-time data ingestion and historical analysis without relying on external hardware.

## Demand Forecasting

Short-horizon electricity demand is predicted using time-series regression techniques. Rolling statistical features such as recent average load and time-of-day indicators are used to forecast total demand for the next 15 minutes. The prediction model achieves a Mean Absolute Error of approximately 0.98 kW, demonstrating reliable short-term forecasting suitable for control decisions.

## Load Balancing Logic

A priority-aware control algorithm evaluates predicted demand against a defined grid capacity limit. When potential peak violations are detected, the system selectively throttles or defers non-critical loads while ensuring that high-priority machines remain unaffected. This rule-based approach emphasizes safety, explainability, and deterministic behavior, which are critical requirements in industrial environments.

## Cost Analysis

To quantify economic impact, the system applies time-of-use electricity tariffs and compares uninterrupted baseline operation with optimized control behavior. The optimized strategy achieves approximately 20% reduction in peak electricity cost, validating the effectiveness of predictive load balancing under realistic pricing conditions.

## Key Takeaways

This project demonstrates end-to-end system thinking across data acquisition, machine learning, control logic, and cost evaluation. It serves as a practical foundation for smart grid research, industrial energy optimization, and data-driven control systems.
