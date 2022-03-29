package com.skf.labs.graphqlinjections.repository;

import com.skf.labs.graphqlinjections.entity.UserInfo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;


public interface UserInfoRepository extends JpaRepository<UserInfo,Integer>{

    @Query("SELECT u FROM UserInfo u WHERE api_key = ?1")
    UserInfo findUserInfoByApiKey(String api_key);


    @Query("SELECT u FROM UserInfo u WHERE user_id = ?1")
    UserInfo findUserInfoByUserId(int user_id);

}
