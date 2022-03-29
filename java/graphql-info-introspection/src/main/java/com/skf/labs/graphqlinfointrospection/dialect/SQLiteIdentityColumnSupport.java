package com.skf.labs.graphqlinfointrospection.dialect;

import org.hibernate.MappingException;
import org.hibernate.dialect.identity.IdentityColumnSupportImpl;

public class SQLiteIdentityColumnSupport extends IdentityColumnSupportImpl {

    @Override
    public boolean supportsIdentityColumns() {
        return true;
    }

    @Override
    public String getIdentitySelectString(String table, String column, int type) throws MappingException {
        return "select MAX(id)";
    }

    @Override
    public String getIdentityColumnString(int type) throws MappingException {
        return "";
    }
}
