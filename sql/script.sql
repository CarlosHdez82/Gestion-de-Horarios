-- =============================
-- USERS (System access)
-- =============================
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INTEGER REFERENCES roles(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================
-- FACULTIES
-- =============================
CREATE TABLE faculties (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- =============================
-- PROGRAMS
-- =============================
CREATE TABLE programs (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    faculty_id INTEGER REFERENCES faculties(id) ON DELETE CASCADE
);

-- =============================
-- TEACHER LEVELS
-- =============================
CREATE TABLE teacher_levels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- =============================
-- TEACHERS
-- =============================
CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(120) UNIQUE,
    phone VARCHAR(20),
    hire_date DATE,
    faculty_id INTEGER REFERENCES faculties(id),
    program_id INTEGER REFERENCES programs(id),
    level_id INTEGER REFERENCES teacher_levels(id),
    role_id INTEGER REFERENCES roles(id),
    is_active BOOLEAN DEFAULT TRUE
);

-- =============================
-- TEACHER DEGREES
-- =============================
CREATE TABLE teacher_degrees (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER REFERENCES teachers(id) ON DELETE CASCADE,
    degree_type VARCHAR(20) NOT NULL, -- Bachelor's, Master's, PhD
    title VARCHAR(100) NOT NULL,
    institution VARCHAR(100) NOT NULL
);

-- =============================
-- SPECIALTIES
-- =============================
CREATE TABLE specialties (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

-- MANY TO MANY: TEACHER - SPECIALTY
CREATE TABLE teacher_specialties (
    teacher_id INTEGER REFERENCES teachers(id) ON DELETE CASCADE,
    specialty_id INTEGER REFERENCES specialties(id) ON DELETE CASCADE,
    PRIMARY KEY (teacher_id, specialty_id)
);

-- =============================
-- SUBJECTS
-- =============================
CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    credits INTEGER CHECK (credits > 0),
    program_id INTEGER REFERENCES programs(id),
    is_active BOOLEAN DEFAULT TRUE
);

-- =============================
-- GROUPS
-- =============================
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    section VARCHAR(10),
    shift VARCHAR(20),
    num_students INTEGER CHECK (num_students >= 0),
    subject_id INTEGER REFERENCES subjects(id)
);

-- =============================
-- ACADEMIC PERIODS
-- =============================
CREATE TABLE academic_periods (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- =============================
-- CLASSROOM TYPES
-- =============================
CREATE TABLE classroom_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- =============================
-- CLASSROOMS
-- =============================
CREATE TABLE classrooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL,
    capacity INTEGER CHECK (capacity > 0),
    location VARCHAR(20), -- B1, B2, B3 etc
    type_id INTEGER REFERENCES classroom_types(id),
    is_active BOOLEAN DEFAULT TRUE
);

-- =============================
-- TEACHER AVAILABILITY
-- =============================
CREATE TABLE teacher_availability (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
    period_id INTEGER NOT NULL REFERENCES academic_periods(id) ON DELETE CASCADE,
    day_of_week VARCHAR(15) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL
);

-- =============================
-- SCHEDULES (Final Assignments)
-- =============================
CREATE TABLE schedules (
    id SERIAL PRIMARY KEY,
    teacher_id INTEGER NOT NULL REFERENCES teachers(id),
    subject_id INTEGER NOT NULL REFERENCES subjects(id),
    group_id INTEGER REFERENCES groups(id),
    classroom_id INTEGER NOT NULL REFERENCES classrooms(id),
    period_id INTEGER NOT NULL REFERENCES academic_periods(id),
    day_of_week VARCHAR(15) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);