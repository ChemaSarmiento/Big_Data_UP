--Get employee dabase
--git clone https://github.com/datacharmer/test_db.git
--cd test_db/
--mysql -usqoop_user -pexample123 < employees.sql


select * from departments;
select * from titles limit 15;
select distinct title from titles;
select distinct first_name, last_name from employees;
select distinct count( first_name, last_name) from employees;

 select count( distinct  concat(first_name , last_name)) from employees;
 

select count(*) from departments;
select count(*) from dept_manager;
select count(*) from dept_manager, departments;                                                         

select * from employees, salaries where employees.emp_no = salaries.emp_no limit 10;
select * from employees, salaries where employees.emp_no = salaries.emp_no order by employees.emp_no, salaries.to_date limit 10;


select * from employees e, salaries s where e.emp_no = s.emp_no order by e.emp_no, s.to_date limit 10;
select * from employees e, salaries s where e.emp_no = s.emp_no and e.emp_no=10001 order by s.to_date;

select e.emp_no, max(salary) from employees e, salaries s where e.emp_no = s.emp_no and e.emp_no=10001 group by e.emp_no;
select e.emp_no, max(salary) from employees e, salaries s where e.emp_no = s.emp_no group by e.emp_no limit 20;

* select t.title, max(s.salary), min(s.salary), avg(s.salary), std(s.salary) from employees e, salaries s, titles t where e.emp_no=s.emp_no and e.emp_no=t.emp_no group by t.title;

select distinct d.dept_no, t.title from employees e, titles t, dept_emp de, departments d where e.emp_no=t.emp_no and e.emp_no=de.emp_no and de.emp_no=d.dept_no=de.dept_no order by d.dept_no, t.title;
select count(*) from (select e.emp_no, count(*) from employees e inner join titles t on e.emp_no=t.emp_no group by e.emp_no having count(*) > 2) tc;

*select d.dept_name, concat(e.first_name , ' ' ,e.last_name) from departments d, dept_manager dm, employees e where d.dept_no=dm.dept_no and dm.emp_no=e.emp_no;

*select  concat(first_name , ' ' , last_name), count(*) from employees group by  concat(first_name , last_name) having count(*) >2;



