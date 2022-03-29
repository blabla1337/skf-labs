package com.skf.labs.graphqlmutation.repository;
import com.skf.labs.graphqlmutation.entity.User;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;


public interface UserRepository extends JpaRepository<User,Integer>{

    @Query("SELECT u FROM User u WHERE username = ?1 AND password = ?2")
    User findUserByUsernamePassword(String username, String password);
}
